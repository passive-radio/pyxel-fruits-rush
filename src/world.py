from typing import Type, TypeVar
from dataclasses import dataclass, field
from component import Component

version = '0.1.dev'

class World():
    def __init__(self):
        self.components = {}
        self.entities = {}
        self.next_entity_id = 0
        self.systems = {}
        self._get_component_cache = {}
        self._get_components_cache = {}
        self.running = True
        
    def create_entity(self,):
        entity = self.next_entity_id
        self.next_entity_id += 1
        return entity
    
    def add_component_to_entity(self, entity, component) -> None:
        component_type = type(component)
        if component_type not in self.components:
            self.components[component_type] = set()
        
        if entity not in self.entities:
            self.entities[entity] = {}
            
        """
        Add entity id in the components[component_type] set where every entities which have the component: component_type is stored.
        Add component in the entities[entity] dict where every components which consists the entit stored.
        """
        self.components[component_type].add(entity)
        self.entities[entity].setdefault(component_type, component)
        
    def get_entity_object(self, entity: int):
        return self.entities[entity]
    
    def _get_component(self, component_type: Component):
        for entity in self.components.get(component_type):
            yield entity, self.entities[entity][component_type]

    def get_component(self, component_type: Component):
        return self._get_component_cache.setdefault(component_type, list(
            self._get_component(component_type))
            )
    
    def _get_components(self, *component_types: list[Component]):
        for entity in set.intersection(*[self.components[ct] for ct in component_types]):
            yield entity, [self.entities[entity][ct] for ct in component_types]
        
    def get_components(self, *component_types: list[Component]):
        return self._get_components_cache.setdefault(component_types, list(self._get_components(*component_types)))
    
    def add_system(self, system, priority: int = 0) -> None:
        system.priority = priority
        system.world = self
        self.systems.append(system)
        self.systems.sort(key=lambda proc: proc.priority, reverse=True)
        print(self.systems)
        
    def process(self):
        for i in range(len(self.systems)):
            self.systems[i].process()
        
    def has_component(self, entity: int, component_type: Component):
        return component_type in self.entities[entity]
