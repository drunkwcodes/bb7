import importlib

# `import litellm` takes 1.5 seconds, defer it!


class LazyLiteLLM:
    _lazy_module = None

    def __getattr__(self, name):
        self._load_litellm()
        return getattr(self._lazy_module, name)

    def _load_litellm(self):
        if self._lazy_module is not None:
            return

        self._lazy_module = importlib.import_module("litellm")

        self._lazy_module.suppress_debug_info = True
        self._lazy_module.set_verbose = False
        self._lazy_module.drop_params = True


litellm = LazyLiteLLM()

__all__ = [litellm]
