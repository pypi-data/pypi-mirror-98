__version__ = '0.000.1'
try:
    from ._LRphase import longest  # noqa
except ImportError:
    def longest(args):
        """
        Args:
            args:
        """
        return max(args, key=len)