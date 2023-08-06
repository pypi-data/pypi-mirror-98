import base64
import asyncio
import posixpath
import json
import re
import time
import random
import string
import weakref

from aiohttp.web_exceptions import HTTPOk

from yarl import URL
from cachetools import LRUCache

from urllib.parse import urlencode

from galacteek import AsyncSignal
from galacteek import ensure
from galacteek import ensureLater
from galacteek import log
from galacteek import loopTime
from galacteek.core import SingletonDecorator
from galacteek.config import cGet

from galacteek.ipfs.wrappers import ipfsOp
from galacteek.ipfs.cidhelpers import cidValid
from galacteek.ipfs.cidhelpers import stripIpfs
from galacteek.ipfs.cidhelpers import joinIpns
from galacteek.ipfs.cidhelpers import IPFSPath
from galacteek.ipfs.dag import DAGOperations
from galacteek.ipfs.encrypt import IpfsRSAAgent
from galacteek.did import ipidIdentRe
from galacteek.did import didExplode
from galacteek.did import normedUtcDate
from galacteek.ld.ldloader import aioipfs_document_loader
from galacteek.ld import asyncjsonld as jsonld
from galacteek.ld.jsonldexpand import ExpandedJSONLDQuerier
from galacteek.core import utcDatetimeIso
from galacteek.core import nonce
from galacteek.core import unusedTcpPort
from galacteek.core.asynclib import async_enterable
from galacteek.core.asynccache import amlrucache
from galacteek.crypto.rsa import RSAExecutor


def ipidFormatValid(did):
    return ipidIdentRe.match(did)


class IPIDException(Exception):
    pass


class IPIDServiceException(Exception):
    pass


class IPServiceRegistry(type):
    IPSREGISTRY = {}

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        cls.IPSREGISTRY[new_cls.__name__] = new_cls
        return new_cls

    @classmethod
    def get_registry(cls):
        return dict(cls.IPSREGISTRY)


class IPServiceEditor(object):
    def __init__(self, ipid, service, sync=True):
        self.ipid = ipid
        self.service = service
        self.sync = sync

    async def __aenter__(self):
        log.debug('Editing Service: {}'.format(self.service.get('id')))
        return self

    async def __aexit__(self, *args):
        if self.sync is True:
            await self.ipid.flush()

        await self.ipid.sServicesChanged.emit()


class IPService(metaclass=IPServiceRegistry):
    """
    InterPlanetary Service (attached to an IPID)
    """

    # Service constants

    SRV_TYPE_DWEBBLOG = 'DwebBlogService'
    SRV_TYPE_DWEBSITE_GENERIC = 'GenericDwebSiteService'
    SRV_TYPE_GALLERY = 'DwebGalleryService'
    SRV_TYPE_ATOMFEED = 'DwebAtomFeedService'
    SRV_TYPE_AVATAR = 'DwebAvatarService'

    SRV_TYPE_PASSPORT = 'DwebPassportService'

    SRV_TYPE_VC = 'VerifiableCredentialService'
    SRV_TYPE_GENERICPYRAMID = 'GalacteekPyramidService'
    SRV_TYPE_CHAT = 'GalacteekChatService'
    SRV_TYPE_PSRENDEZVOUS = 'PSRendezVousService'
    SRV_TYPE_VIDEOCALL = 'DwebVideoCallService'

    SRV_TYPE_LIVEPEER_STREAMING = 'P2PLivePeerStreamingService'

    SRV_TYPE_COLLECTION = 'ObjectsCollectionService'

    forTypes = []
    container = False

    def __init__(self, dagNode: dict, ipid):
        self._srv = dagNode
        self._didEx = didExplode(self.id)
        self._ipid = ipid

        self.sChanged = AsyncSignal()
        self.sChanged.connectTo(self.onChanged)

    @property
    def ipid(self):
        return self._ipid

    @property
    def ipidServiceUrl(self):
        try:
            return URL.build(
                scheme='ipid',
                host=self.srvIpId,
                path=self.srvPath,
                fragment=self.srvFragment
            )
        except Exception:
            return None

    @property
    def id(self):
        return self._srv['id']

    @property
    def description(self):
        return self._srv.get('description', 'No description')

    @property
    def pubdate(self):
        return self._srv.get('datepublished')

    @property
    def srvIpId(self):
        return self._didEx['id'] if self._didEx else None

    @property
    def srvFragment(self):
        return self._didEx['fragment'] if self._didEx else None

    @property
    def srvPath(self):
        return self._didEx['path'] if self._didEx else None

    @property
    def type(self):
        return self._srv['type']

    @property
    def endpoint(self):
        return self._srv['serviceEndpoint']

    async def expandEndpoint(self):
        exSrv = await self.ipid.expandService(self.id)
        if not exSrv:
            return None

        try:
            return exSrv.get('https://w3id.org/did#serviceEndpoint')[0]
        except Exception:
            return None

    async def expandEndpointLdWizard(self):
        return ExpandedJSONLDQuerier(
            await self.expandEndpoint())

    @ipfsOp
    async def endpointCat(self, ipfsop):
        ipfsPath = IPFSPath(self.endpoint)
        if ipfsPath.valid:
            return await ipfsop.catObject(ipfsPath.objPath)

    async def onChanged(self):
        pass

    async def serviceStart(self):
        pass

    def __repr__(self):
        return self.id

    def __str__(self):
        if self.type == self.SRV_TYPE_DWEBBLOG:
            srvStr = 'User blog'
        elif self.type == self.SRV_TYPE_GALLERY:
            srvStr = 'Image gallery'
        elif self.type == self.SRV_TYPE_GENERICPYRAMID:
            srvStr = 'Generic pyramid'
        elif self.type == self.SRV_TYPE_ATOMFEED:
            srvStr = 'Atom feed'
        elif self.type == self.SRV_TYPE_AVATAR:
            srvStr = 'User avatar'
        else:
            srvStr = 'Unknown service'

        return 'IPS: {srv}'.format(
            srv=srvStr
        )


class IPGenericService(IPService):
    forTypes = [
        IPService.SRV_TYPE_ATOMFEED,
        IPService.SRV_TYPE_DWEBBLOG,
        IPService.SRV_TYPE_DWEBSITE_GENERIC,
        IPService.SRV_TYPE_GALLERY,
        IPService.SRV_TYPE_GENERICPYRAMID,
        IPService.SRV_TYPE_AVATAR
    ]


class CollectionService(IPService):
    forTypes = ['ObjectsCollectionService']
    endpointName = 'ObjectsCollectionEndpoint'
    container = True

    async def getObjectWithId(self, id: str):
        async for obj in self.contained():
            if obj['id'] == id:
                return obj

    async def contained(self):
        endpoint = await self.expandEndpoint()
        if not endpoint:
            return

        for obj in endpoint.get(self.ipid.contextUrl(
                self.endpointName, fragment='objects')):
            try:
                yield {
                    'id': obj['@id'],
                    'path': obj.get(
                        self.ipid.contextUrl(
                            'IpfsObject', fragment='path')
                    )[0]['@value'],
                    'name': obj.get(
                        self.ipid.contextUrl(
                            'IpfsObject', fragment='name')
                    )[0]['@value']
                }
            except Exception:
                continue

    @ipfsOp
    async def add(self, ipfsop, objPath, name=None,
                  description='No description'):
        path = IPFSPath(objPath, autoCidConv=True)
        if not path.valid:
            raise ValueError('Invalid path')

        if not path.isRoot:
            oName = path.basename
        else:
            oName = name if name else hex(int(time.time() * 10000))[2:]

        oId = '{didurl}/{o}'.format(didurl=self.id, o=oName)
        try:
            async with self.ipid.editService(self.id) as editor:
                editor.service['serviceEndpoint']['objects'].append({
                    '@context': await ipfsop.ldContext('IpfsObject'),
                    'id': oId,
                    'objectPath': objPath,
                    'objectName': path.basename,
                    'objectDescription': description
                })

            return True
        except Exception as err:
            self.ipid.message('Error editing collection service: {}'.format(
                str(err)))
            return False

    def __str__(self):
        return 'IPS: Collection ({name})'.format(
            name=self.endpoint.get('name', 'Unknown')
        )


class LivePeerStreamingService(IPService):
    forTypes = [IPService.SRV_TYPE_LIVEPEER_STREAMING]
    endpointName = 'LivePeerEndpoint'


class PSRendezVousService(IPService):
    forTypes = [IPService.SRV_TYPE_PSRENDEZVOUS]
    endpointName = 'PSRendezVousEndpoint'


class IPIdentifier(DAGOperations):
    """
    InterPlanetary IDentifier (decentralized identity)

    This tries to follow the IPID spec as much as possible.
    """

    def __init__(self, did, localId=False, ldCache=None):
        self._did = did
        self._p2pServices = weakref.WeakValueDictionary()
        self._document = {}
        self._docCid = None
        self._localId = localId
        self._lastResolve = None
        self._latestModified = None
        self._unlocked = False
        self.rsaAgent = None

        # JSON-LD expanded cache
        self.cache = ldCache if ldCache else LRUCache(4)

        # Async sigs
        self.sChanged = AsyncSignal(str)
        self.sServicesChanged = AsyncSignal()
        self.sServiceAvailable = AsyncSignal(IPIdentifier, IPService)
        self.sChanged.connectTo(self.onDidChanged)

    @property
    def local(self):
        return self._localId is True

    @property
    def unlocked(self):
        return self._unlocked

    @property
    def dagCid(self):
        return self.docCid

    @property
    def docCid(self):
        return self._docCid

    @docCid.setter
    def docCid(self, cid):
        self.message('Updating DIDDoc CID from {prev} to {n}'.format(
            prev=self._docCid, n=cid))

        if cidValid(cid):
            self._docCid = cid

    @property
    def doc(self):
        return self._document

    @property
    def did(self):
        return self._did

    @property
    def p2pServices(self):
        return self._p2pServices

    @property
    def id(self):
        return self.ipnsKey

    @property
    def ipnsKey(self):
        exploded = didExplode(self.did)
        if exploded and exploded['method'] == 'ipid':
            return exploded['id']

    @property
    def latestModified(self):
        return self._latestModified

    def contextUrl(self, path, fragment=None):
        return str(
            URL.build(
                host='galacteek.ld.contexts',
                scheme='ipschema',
                path='/' + path,
                fragment=fragment
            )
        )

    def message(self, msg, level='debug'):
        getattr(log, level)('IPID ({loc}) ({did}): {msg}'.format(
            did=self.did, msg=msg, loc='local' if self._localId else 'net'))

    def didFragment(self, frag):
        return self.didUrl(fragment=frag)

    def didUrl(self, params=None, path=None,
               query=None, fragment=None):
        """
        Build a DID URL with the given params
        """

        url = '{did}'.format(did=self.did)

        if isinstance(params, dict):
            p = ['{0}={1}'.format(k, str(v)) for k, v in params.items()]
            url += ';' + ';'.join(p)

        if isinstance(path, str):
            # url += path
            if not path.startswith('/'):
                url += f'/{path}'
            else:
                url += path

        if isinstance(query, dict):
            url += '?' + urlencode(query)

        if isinstance(fragment, str):
            if not fragment.startswith('#'):
                url += '#' + fragment
            else:
                url += fragment

        return url

    def dump(self):
        """
        Dump the DID document to stdout
        """

        print(json.dumps(self.doc, indent=4))

    async def onDidChanged(self, cid):
        cacheKey = repr(self)
        if cacheKey in self.cache:
            # Reset expanded cache
            self.message('LRU cache reset')
            del self.cache[cacheKey]

    @ipfsOp
    async def unlock(self, ipfsop, rsaPassphrase=None):
        rsaAgent = await self.rsaAgentGet(ipfsop)
        if not rsaAgent:
            raise Exception('Agent')

        if await rsaAgent.privKeyUnlock(passphrase=rsaPassphrase):
            self._unlocked = True
        else:
            self._unlocked = False

        return self.unlocked

    async def rsaAgentGet(self, ipfsop):
        curProfile = ipfsop.ctx.currentProfile

        if self.rsaAgent:
            return self.rsaAgent

        if self.local:
            privKeyPath = curProfile._didKeyStore._privateKeyPathForDid(
                self.did)

            if not privKeyPath:
                raise Exception('Cannot find private DID key')

            pubKeyPem = await self.pubKeyPemGet(idx=0)

            self.rsaAgent = IpfsRSAAgent(
                ipfsop.ctx.rsaExec, pubKeyPem, privKeyPath)
            return self.rsaAgent

    @ipfsOp
    async def pssSign64(self, ipfsop, message: bytes):
        agent = await self.rsaAgentGet(ipfsop)
        if agent:
            return await agent.pssSign64(message)

    @ipfsOp
    async def pssVerif(self, ipfsop, message: bytes, signature: bytes):
        pubKeyPem = await self.pubKeyPemGet(idx=0)
        if pubKeyPem:
            return await ipfsop.ctx.rsaExec.pssVerif(
                message, signature, pubKeyPem)

    @ipfsOp
    async def inline(self, ipfsop, path=''):
        # In-line the JSON-LD contexts in the DAG for JSON-LD usage

        return await ipfsop.ldInline(await self.get(path=path))

    @ipfsOp
    async def compact(self, ipfsop):
        pass

    @amlrucache
    async def expand(self):
        return await self._expand()

    @ipfsOp
    async def _expand(self, ipfsop, path=''):
        """
        Perform a JSON-LD expansion on the DID document
        """

        try:
            expanded = await jsonld.expand(await self.inline(path=path), {
                'documentLoader': await aioipfs_document_loader(ipfsop.client)
            })

            if isinstance(expanded, list) and len(expanded) > 0:
                return expanded[0]
        except Exception as err:
            self.message('Error expanding DID document: {}'.format(
                str(err)))

    @ipfsOp
    async def expandService(self, ipfsop, srvId):
        try:
            expanded = await self.expand()
            if not expanded:
                return None

            for srv in expanded.get('https://w3id.org/did#service', []):
                if srv.get('@id') == srvId:
                    return srv
        except Exception:
            pass

    async def update(self, obj: dict, publish=False):
        self._document.update(obj)
        await self.updateDocument(self.doc, publish=publish)

    async def flush(self):
        await self.updateDocument(self.doc, publish=True)

    async def servicePropagate(self, service: IPService):
        log.debug(f'Propagating IP service: {service}')

        await self.sServiceAvailable.emit(self, service)

    async def addServiceRaw(self, service: dict, publish=True):
        sid = service.get('id')
        assert isinstance(sid, str)

        didEx = didExplode(sid)
        assert didEx is not None

        if await self.searchServiceById(sid) is not None:
            raise IPIDServiceException(
                'An IP service already exists with this ID')

        self._document['service'].append(service)
        await self.updateDocument(self.doc, publish=publish)
        await self.sServicesChanged.emit()

        return self._serviceInst(service)

    @ipfsOp
    async def addServiceContexted(self, ipfsop, service: dict,
                                  endpoint=None,
                                  publish=True,
                                  context='IpfsObjectEndpoint'):
        sid = service.get('id')
        assert isinstance(sid, str)

        didEx = didExplode(sid)
        assert didEx is not None

        if await self.searchServiceById(sid) is not None:
            raise IPIDServiceException(
                'An IP service already exists with this ID')

        srvCtx = await ipfsop.ldContext(context)

        if srvCtx:
            service['serviceEndpoint'] = {
                '@context': srvCtx
            }

            if isinstance(endpoint, dict):
                service['serviceEndpoint'].update(endpoint)

            self._document['service'].append(service)
            await self.updateDocument(self.doc, publish=publish)
            await self.sServicesChanged.emit()

            sInst = self._serviceInst(service)
            await self.servicePropagate(sInst)

            return sInst
        else:
            raise Exception('Could not initiate service context')

    @ipfsOp
    async def addServiceCollection(self, ipfsop, name):
        return await self.addServiceContexted({
            'id': self.didUrl(
                path=posixpath.join('/collections', name)
            ),
            'type': IPService.SRV_TYPE_COLLECTION,
        }, context='ObjectsCollectionEndpoint',
            endpoint={
            'name': name,
            'created': utcDatetimeIso(),
            'objects': []
        }, publish=True)

    @ipfsOp
    async def addServiceRendezVous(self, ipfsop):
        serviceName = 'ps-rendezvous'
        return await self.addServiceRaw({
            'id': self.didUrl(
                path=f'/{serviceName}'
            ),
            'type': IPService.SRV_TYPE_PSRENDEZVOUS,
            'description': 'PubSub rendezvous',
            'serviceEndpoint': ipfsop.p2pEndpoint(serviceName)
        })

    @ipfsOp
    async def addServiceVideoCall(self, ipfsop, roomName):
        servicePath = posixpath.join('videocall', roomName)

        return await self.addServiceContexted({
            'id': self.didUrl(
                path=servicePath
            ),
            'type': IPService.SRV_TYPE_VIDEOCALL,
        }, context='DwebVideoCallServiceEndpoint',
            endpoint={
            'roomName': roomName,
            'created': utcDatetimeIso(),
            'p2pEndpoint': ipfsop.p2pEndpoint(servicePath)
        }, publish=True)

    @ipfsOp
    async def updateDocument(self, ipfsop, document, publish=False):
        """
        Update the document and set the 'previous' IPLD link
        """

        now = normedUtcDate()
        self._document = document

        if self.docCid:
            self._document['previous'] = {
                '/': self.docCid
            }

        self._document['updated'] = now

        cid = await ipfsop.dagPut(document)

        if cid:
            self.docCid = cid

            if publish:
                ensure(self.publish())

            await self.sChanged.emit(cid)
        else:
            self.message('Could not inject new DID document!')

    @ipfsOp
    async def resolve(self, ipfsop, resolveTimeout=None):
        resolveTimeout = resolveTimeout if resolveTimeout else \
            cGet('resolve.timeout')

        if self.local:
            hours = cGet('resolve.cacheLifetime.local.hours')
        else:
            hours = cGet('resolve.cacheLifetime.default.hours')

        maxLifetime = hours * 3600

        useCache = 'always'
        cache = 'always'

        self.message('DID resolve: {did} (using cache: {usecache})'.format(
            did=self.ipnsKey, usecache=useCache))

        return await ipfsop.nameResolveStreamFirst(
            joinIpns(self.ipnsKey),
            count=1,
            timeout=resolveTimeout,
            useCache=useCache,
            cache=cache,
            cacheOrigin='ipidmanager',
            maxCacheLifetime=maxLifetime
        )

    async def refresh(self):
        staleValue = cGet('resolve.staleAfterDelay')
        last = self._lastResolve

        if self.local or not last or (loopTime() - last) > staleValue:
            self.message('Reloading')

            return await self.load()

    @ipfsOp
    async def load(self, ipfsop, pin=True, initialCid=None,
                   resolveTimeout=30):
        if not initialCid:
            resolved = await self.resolve()

            if not resolved:
                self.message('Failed to resolve ?')
                return False

            dagCid = stripIpfs(resolved['Path'])
        else:
            self.message('Loading from initial CID: {}'.format(initialCid))
            dagCid = initialCid

        self.message('DID resolves to {}'.format(dagCid))

        if self.docCid == dagCid:
            # We already have this one

            self.message('DID document already at latest iteration')
            return False

        self._lastResolve = loopTime()

        if pin is True:
            await ipfsop.ctx.pin(dagCid, qname='ipid')

        self.message('Load: IPNS key resolved to {}'.format(dagCid))

        doc = await ipfsop.dagGet(dagCid)

        if doc:
            self._document = doc
            self._latestModified = doc.get('modified')
            self.docCid = dagCid
            await self.sChanged.emit(dagCid)

            if self.local:
                # Local IPID: propagate did services
                async for service in self.discoverServices():
                    await self.sServiceAvailable.emit(self, service)

            return True

        return False

    @ipfsOp
    async def publish(self, ipfsop, timeout=None):
        """
        Publish the DID document to the IPNS key

        We always cache the record so that your DID is always
        resolvable whatever the connection state.

        :rtype: bool
        """

        # Get config settings
        timeout = timeout if timeout else cGet('publish.ipns.timeout')
        autoRepublish = cGet('publish.autoRepublish')
        republishDelay = cGet('publish.autoRepublishDelay')

        ipnsLifetime = cGet('publish.ipns.lifetime')
        ipnsTtl = cGet('publish.ipns.ttl')

        if not self.docCid:
            return False

        if autoRepublish is True:
            # Auto republish for local IPIDs
            ensureLater(
                republishDelay,
                self.publish
            )

        try:
            if await ipfsop.publish(self.docCid,
                                    key=self.ipnsKey,
                                    lifetime=ipnsLifetime,
                                    ttl=ipnsTtl,
                                    cache='always',
                                    cacheOrigin='ipidmanager',
                                    timeout=timeout):
                self.message('Published !')
                self.message(
                    'Published IPID {did} with docCid: {docCid}'.format(
                        did=self.did, docCid=self.docCid))
                return True
            else:
                self.message('Error publishing IPID with DID: {did}'.format(
                    did=self.did))
                return False
        except Exception as e:
            self.message(str(e))
            return False

    @ipfsOp
    async def dagGet(self, ipfsop, path):
        if self.docCid:
            dPath = posixpath.join(self.docCid, path)
            self.message('DID docget: {}'.format(dPath))

            try:
                return await ipfsop.dagGet(dPath)
            except Exception as err:
                self.message('DAG get error for {p}: {err}'.format(
                    p=dPath, err=str(err)))
        else:
            self.message('DAG get impossible (no DID document yet)')

    async def pubKeys(self):
        """
        Async generator that yields each publicKey
        """
        for pKey in await self.dagGet('publicKey'):
            yield pKey

    async def pubKeyWithId(self, id: str):
        """
        Get first publicKey that matches the id

        :param str id: PublicKey id
        """

        async for pKey in self.pubKeys():
            if pKey.get('id') == id:
                return pKey

    async def pubKeyGet(self, idx=0):
        """
        Returns the publicKey node with the idx index in the array

        :param int idx: Public key index
        :rtype: dict
        """
        return await self.dagGet('publicKey/{}'.format(idx))

    async def pubKeyPemGet(self, idx=0):
        """
        Returns the publicKey PEM with the idx index in the array

        :rtype: str
        """
        return await self.dagGet('publicKey/{}/publicKeyPem'.format(idx))

    async def pubKeyPemGetWithId(self, keyId):
        """
        Returns the publicKey PEM whose id matches keyId

        :rtype: str
        """

        for key in await self.dagGet('publicKey'):
            if key.get('id') == keyId:
                return key['publicKeyPem']

    async def getServices(self):
        node = await self.dagGet('service')
        return node if node else []

    def _serviceInst(self, srv):
        stype = srv.get('type')

        for cname, sclass in IPServiceRegistry.IPSREGISTRY.items():
            if stype in sclass.forTypes:
                return sclass(srv, self)

    async def discoverServices(self):
        for srv in await self.getServices():
            _inst = self._serviceInst(srv)
            if _inst:
                yield _inst

    async def getServiceByType(self, srvType: str):
        """
        Get first service found that matches the service type

        :param str srvType: Service type
        """

        for srv in await self.getServices():
            if srv.get('type') == srvType:
                return IPService(srv, self)

    async def searchServices(self, query: str):
        for srvNode in await self.getServices():
            service = IPService(srvNode, self)

            if re.search(query, service.id, re.IGNORECASE):
                yield service

    async def searchServiceById(self, _id: str):
        for srvNode in await self.getServices():
            if srvNode['id'] == _id:
                _inst = self._serviceInst(srvNode)
                if _inst:
                    return _inst

            await asyncio.sleep(0)

    async def removeServiceById(self, _id: str):
        """
        Remove the service with the given DID identifier
        """
        try:
            for srv in self._document['service']:
                if srv['id'] == _id:
                    self._document['service'].remove(srv)
                    await self.flush()
        except Exception as err:
            log.debug(str(err))

    async def avatarService(self):
        avatarServiceId = self.didUrl(path='/avatar')
        return await self.searchServiceById(avatarServiceId)

    async def avatarSet(self, ipfsPath):
        avatarServiceId = self.didUrl(path='/avatar')

        if not await self.avatarService():
            await self.addServiceRaw({
                'id': avatarServiceId,
                'type': IPService.SRV_TYPE_AVATAR,
                'serviceEndpoint': str(ipfsPath),
                'description': 'User Avatar'
            }, publish=True)
        else:
            async with self.editService(avatarServiceId) as editor:
                editor.service['serviceEndpoint'] = str(ipfsPath)

    @async_enterable
    async def editService(self, _id: str, sync=True):
        """
        Edit the IP service with the given ID

        Returns an async context which flushes the DID document
        by default on leaving the context
        """
        for srv in self._document['service']:
            if srv['id'] == _id:
                return IPServiceEditor(self, srv, sync=sync)

    async def _stopP2PServices(self):
        for srvName, srv in self._p2pServices.items():
            await srv.stop()

    async def _stop(self):
        await self._stopP2PServices()

    def __eq__(self, other):
        return self.did == other.did

    def __repr__(self):
        return self.did

    def __str__(self):
        return 'IP Identifier: {did}'.format(did=self.did)


@SingletonDecorator
class IPIDManager:
    def __init__(self):
        self._managedIdentifiers = {}
        self._lock = asyncio.Lock()
        self._resolveTimeout = cGet('resolve.timeout')
        self._rsaExec = RSAExecutor()

        # JSON-LD cache
        self._ldCache = LRUCache(256)

    async def stopManager(self):
        async with self._lock:
            for didIdentifier, ipid in self._managedIdentifiers.items():
                if ipid.local:
                    log.debug(f'Stopping DID: {didIdentifier}')
                    await ipid._stop()

    async def onLocalIpidServiceAvailable(self, ipid, ipService):
        await ipService.serviceStart()

    async def track(self, ipid: IPIdentifier):
        async with self._lock:
            self._managedIdentifiers[ipid.did] = ipid

    async def searchServices(self, term: str):
        async with self._lock:
            for did, ipid in self._managedIdentifiers.items():
                async for srv in ipid.searchServices(term):
                    yield srv

                await asyncio.sleep(0)

    async def getServiceById(self, _id: str):
        async with self._lock:
            for did, ipid in self._managedIdentifiers.items():
                srv = await ipid.searchServiceById(_id)
                if srv:
                    return srv

                await asyncio.sleep(0)

    async def trackingTask(self):
        while True:
            await asyncio.sleep(60 * 5)

            async with self._lock:
                for did, ipId in self._managedIdentifiers.items():
                    await ipId.load()
                    log.debug('tracker: {0} => {1}'.format(
                        ipId, ipId.docCid))

    @ipfsOp
    async def load(self, ipfsop,
                   did: str,
                   timeout=None,
                   localIdentifier=False,
                   initialCid=None,
                   track=True):

        if not did or not ipidFormatValid(did):
            return None

        async with self._lock:
            if did in self._managedIdentifiers:
                return self._managedIdentifiers[did]

        rTimeout = timeout if timeout else self._resolveTimeout

        ipid = IPIdentifier(
            did, localId=localIdentifier, ldCache=self._ldCache)

        if ipid.local:
            ipid.sServiceAvailable.connectTo(
                self.onLocalIpidServiceAvailable)

        if await ipid.load(resolveTimeout=rTimeout, initialCid=initialCid):
            if track:
                await self.track(ipid)

            if localIdentifier:
                log.debug('Publishing (first load) local IPID: {}'.format(did))
                ensure(ipid.publish())

            return ipid

    @ipfsOp
    async def create(self, ipfsop,
                     ipnsKeyName: str,
                     pubKeyPem=None,
                     purgeKey=True,
                     track=True):
        """
        Create a DID with the IPID method

        :param str ipnsKeyName: IPNS key name to use
        :param str pubKeyPem: RSA PubKey PEM
        :param bool purgeKey: Remove IPNS key if it already exists
        """
        names = await ipfsop.keysNames()

        if ipnsKeyName in names and purgeKey:
            await ipfsop.keysRemove(ipnsKeyName)

        ipnsKey = await ipfsop.keyGen(ipnsKeyName)
        if ipnsKey is None:
            raise IPIDException('Cannot create IPNS Key')

        ipnsKeyId = ipnsKey['Id']

        didId = "did:ipid:{key}".format(key=ipnsKeyId)

        log.debug('Generating DID document with DID: {}'.format(didId))

        now = normedUtcDate()

        identifier = IPIdentifier(didId, localId=True)

        # Initial document
        initialDoc = {
            "@context": await ipfsop.ldContext('did-v0.11'),
            "publicKey": [{
                "id": "{did}#keys-1".format(did=didId),
                "type": "RsaVerificationKey2018",
                "controller": didId,
                "publicKeyPem": pubKeyPem
            }],
            "service": [],
            "created": now,
            "updated": now
        }

        await identifier.updateDocument(initialDoc)

        # Update the document with the IPID and auth section
        await identifier.update({
            'id': didId,
            "authentication": [{
                "id": "{did}#keys-1".format(did=didId),
                "type": "RsaSignatureAuthentication2018",
                "controller": didId,
                "publicKey": [
                    didId
                ]
            }]
        })

        # Publish the DID document to the key
        ensure(identifier.publish())

        if track:
            await self.track(identifier)

        # Register default IP services
        # for service in ipfsop.ctx.p2p.services:
        #     if service.didDefaultRegister:
        #         await service.didServiceInstall(identifier)

        return identifier

    @ipfsOp
    async def didAuthenticate(self, ipfsop, ipid: IPIdentifier, peerId,
                              token=None):
        log.debug('DID auth for {}'.format(ipid))
        lPort = unusedTcpPort()

        if not lPort:
            return

        async with ipfsop.p2pDialer(
                peerId, 'didauth-vc-pss',
                addressAuto=True) as streamCtx:
            if streamCtx.failed:
                return False
            else:
                log.debug(
                    f'DID Authenticate ({ipid.did}): connected to service')
                await ipfsop.sleep(0.5)

                return await self.didAuthPerform(
                    ipfsop, streamCtx, ipid, token=token)

    async def didAuthPerform(self, ipfsop, streamCtx, ipid, token=None):
        rand = random.Random()
        req = {
            'challenge': ''.join(
                [str(rand.choice(string.ascii_letters)) for x in range(
                    0, rand.randint(256, 384))]),
            'did': ipid.did,
            'nonce': nonce()
        }

        if token:
            req['ident_token'] = token

        try:
            async with streamCtx.session as session:
                async with session.post(
                        streamCtx.httpUrl('/auth'),
                        data=json.dumps(req)) as resp:
                    if resp.status != HTTPOk.status_code:
                        payload = await resp.json()
                        log.debug(f'Error payload: {payload}')
                        raise Exception(f'DID Auth error: code {resp.status}')

                    payload = await resp.json()

                    # Expand the response and verify it

                    async with ipfsop.ldOps() as ldCtx:
                        expanded = await ldCtx.expandDocument(payload)
                        if not expanded:
                            raise Exception('Invalid IPLD document')

                    return await self.vcLdValidate(
                        ipid, req, expanded
                    )
        except Exception as err:
            log.debug(f'didAuthPerform error: {err}')
            return False

    @ipfsOp
    async def vcLdValidate(self, ipfsop, ipid, req, document):
        """ Validate the verifiable credentials """

        try:
            issued = document.get(
                'https://www.w3.org/2018/credentials#issued')[0]['@value']
            assert issued is not None

            # Issuer's DID
            issuer = document.get(
                'https://www.w3.org/2018/credentials#issuer')[0]['@id']
            assert issuer == req['did']

            # Credential Subject
            cSubject = document.get(
                'https://www.w3.org/2018/credentials#'
                'credentialSubject')[0]['@id']
            assert cSubject == req['did']

            # Get the proof and check the type and nonce
            proof = document.get(
                'https://w3id.org/security#proof')[0]['@graph'][0]
            assert proof.get('https://w3id.org/security'
                             '#challenge')[0]['@value'] == req['nonce']
            assert proof['@type'][0] == \
                'https://w3id.org/security#RsaSignature2018'

            assert proof.get(
                'https://w3id.org/security#proofPurpose')[0]['@id'] == \
                'https://w3id.org/security#authenticationMethod'

            sigValue = proof.get(
                'https://w3id.org/security#proofValue')[0]['@value']
            assert isinstance(sigValue, str)

            # IRI: https://w3id.org/security#verificationMethod
            # corresponds to the signer's publicKey DID's id

            vMethod = proof.get(
                'https://w3id.org/security#verificationMethod')[0]['@id']

            rsaPubPem = await ipid.pubKeyPemGetWithId(vMethod)
            if not rsaPubPem:
                log.debug('didAuthPerform: PubKey not found: {}'.format(
                    str(vMethod)))
                return False

            # Check the signature with PSS
            return await self._rsaExec.pssVerif(
                req['challenge'].encode(),
                base64.b64decode(sigValue),
                rsaPubPem
            )
        except AssertionError as aerr:
            log.debug('Verifiable credentials assert error: {}'.format(
                str(aerr)))
            return False
        except Exception as err:
            log.debug('Unknown VC error: {}'.format(str(err)))
            return False
