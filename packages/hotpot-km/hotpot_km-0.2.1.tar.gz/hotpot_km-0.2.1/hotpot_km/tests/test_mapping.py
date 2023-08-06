from contextlib import asynccontextmanager
from subprocess import PIPE

from jupyter_client.kernelspec import NATIVE_KERNEL_NAME
from pytest import mark
from traitlets.config.loader import Config
from tornado.testing import gen_test

from .. import MaximumKernelsException

try:
    from ..mapping import PooledMappingKernelManager
except ImportError:
    pass


from .utils import async_shutdown_all_direct, TestAsyncKernelManager

# Test that it works as normal with default config
class TestMappingKernelManagerUnused(TestAsyncKernelManager):
    __test__ = True

    # static so picklable for multiprocessing on Windows
    @staticmethod
    @asynccontextmanager
    async def _get_tcp_km():
        c = Config()
        km = PooledMappingKernelManager(config=c)
        try:
            yield km
        finally:
            await km.shutdown_all()

    # Mapping manager doesn't handle this:
    @mark.skip()
    @gen_test
    async def test_tcp_lifecycle_with_kernel_id(self):
        pass


# Test that it works with a max that is larger than pool size
class TestMappingKernelManagerApplied(TestAsyncKernelManager):
    __test__ = True

    # static so picklable for multiprocessing on Windows
    @staticmethod
    @asynccontextmanager
    async def _get_tcp_km():
        c = Config()
        c.LimitedKernelManager.max_kernels = 4
        c.PooledMappingKernelManager.fill_delay = 0
        c.PooledMappingKernelManager.kernel_pools = {NATIVE_KERNEL_NAME: 2}
        c.PooledMappingKernelManager.pool_kwargs = {
            NATIVE_KERNEL_NAME: dict(stdout=PIPE, stderr=PIPE)
        }
        km = PooledMappingKernelManager(config=c)
        try:
            await km.wait_for_pool()
            yield km
        finally:
            await km.shutdown_all()

    # Mapping manager doesn't handle this:
    @mark.skip()
    @gen_test
    async def test_tcp_lifecycle_with_kernel_id(self):
        pass

    @gen_test(timeout=60)
    async def test_exceed_pool_size(self):
        async with self._get_tcp_km() as km:
            self.assertEqual(len(km._pools[NATIVE_KERNEL_NAME]), 2)
            kids = []
            for i in range(4):
                kid = await km.start_kernel(stdout=PIPE, stderr=PIPE)
                self.assertIn(kid, km)
                kids.append(kid)
                self.assertEqual(len(km._pools[NATIVE_KERNEL_NAME]), 2)

            await async_shutdown_all_direct(km)
            for kid in kids:
                self.assertNotIn(kid, km)

            # Cycle again to assure the pool survives that
            kids = []
            for i in range(4):
                kid = await km.start_kernel(stdout=PIPE, stderr=PIPE)
                self.assertIn(kid, km)
                kids.append(kid)
                self.assertEqual(len(km._pools[NATIVE_KERNEL_NAME]), 2)

            await km.shutdown_all()
            for kid in kids:
                self.assertNotIn(kid, km)

    @gen_test(timeout=60)
    async def test_breach_max(self):
        async with self._get_tcp_km() as km:
            kids = []
            for i in range(4):
                kid = await km.start_kernel(stdout=PIPE, stderr=PIPE)
                self.assertIn(kid, km)
                kids.append(kid)

            with self.assertRaises(MaximumKernelsException):
                await km.start_kernel(stdout=PIPE, stderr=PIPE)

            # Remove and add one to make sure we correctly recovered
            await km.shutdown_kernel(kid)
            self.assertNotIn(kid, km)
            kids.pop()

            kid = await km.start_kernel(stdout=PIPE, stderr=PIPE)
            self.assertIn(kid, km)
            kids.append(kid)

            await km.shutdown_all()
            for kid in kids:
                self.assertNotIn(kid, km)
