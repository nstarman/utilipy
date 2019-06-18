from wrapt import ObjectProxy
import numpy as np


class CustomObjectProxy(ObjectProxy):

    def __init__(self, wrapped, *_, **kw):
        super().__init__(wrapped)

        for k, v in kw.items():
            setattr(self, '_self_' + k, v)

    def __getattr__(self, name):
        try:
            return super().__getattr__(name)
        except Exception as e:
            return getattr(self, '_self_' + name)

    def proxysetattr(self, name, value):
        setattr(self, '_self_' + name, value)

    def proxysetattrs(self, **kw):
        for k, v in kw.items():
            self.proxysetattr(k, v)


x = CustomObjectProxy(np.linspace(0, 10), color='black', t0=2)
# x._self_color = 'black'

print(x[:10])
print(x**2)
print(x.shape)
print(x._self_color)
print(type(x))
print(x.t0)
