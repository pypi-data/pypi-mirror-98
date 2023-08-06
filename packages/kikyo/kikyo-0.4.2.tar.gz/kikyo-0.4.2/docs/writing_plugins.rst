.. _writing_plugins:

开发插件
================================================================================

插件加载机制
--------------------------------------------------------------------------------

kikyo利用setuptools的entry points特性来发现注册的插件，并通过执行钩子函数完成插件的加载。
kikyo通过名为 ``kikyo.plugins`` 的entry point来发现注册的插件。

编写你自己的插件
--------------------------------------------------------------------------------

如果你希望编写能够被kikyo自动加载，需要在setup.py中定义名为 ``kikyo.plugins`` 的entry point。

.. code-block:: python

    # setup.py示例
    from setuptools import setup

    setup(
        name="plugin_project",
        packages=["plugin_project"],
        entry_points={'kikyo.plugins': 'name_of_plugin = plugin_project.plugin_module'}
    )

当这个Python库安装后，kikyo会将 ``plugin_project.plugin_module`` 作为插件安装。

插件需要在根模块下定义名为 ``configure_kikyo`` 的钩子函数来实现对kikyo客户端的配置：

.. code-block:: python

    from kikyo import Kikyo


    def configure_kikyo(client: Kikyo):
        """配置kikyo客户端"""
