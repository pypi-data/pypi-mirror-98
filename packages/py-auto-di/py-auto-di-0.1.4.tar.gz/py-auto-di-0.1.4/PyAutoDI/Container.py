from .registry_utils import build_dependency_definition, get_dependency_name


class Container:
    def __init__(self):
        self.registry = {}

    def register_by_name(self, name, dependency_class, interface):
        self.registry[name] = build_dependency_definition(
            dependency_class, interface)

    def register(self, dependency_class, interface=None):
        name = get_dependency_name(dependency_class)

        self.register_by_name(name, dependency_class, interface)

    def get_registry_keys(self):
        return self.registry.keys()

    def build_dependencies(self, dependency_names):
        dependencies = []

        for name in dependency_names:
            dependencies.append(self.build(name))

        return dependencies

    def build(self, name):
        dependency_definition = self.registry[name]

        base_class = dependency_definition["dependency_class"]
        dependency_names = dependency_definition["dependency_names"]

        dependencies = self.build_dependencies(dependency_names)

        return base_class(*dependencies)

    def override(self, name, override_class):
        dependency_definition = self.registry[name]
        original_interface = dependency_definition["interface"]

        override_implements_original_interface = (
            original_interface == None or
            issubclass(override_class, original_interface))

        if(not override_implements_original_interface):
            raise Exception(
                "Overriding class does not implement expected interface")

        self.register_by_name(name, override_class, original_interface)

    def new(self):
        new_container = Container()

        registry_keys = self.get_registry_keys()

        for registry_key in registry_keys:
            new_container.register(self.registry[registry_key]["dependency_class"])

        return new_container
