from neo4j import GraphDatabase
from typing import List

class SkillGraphDB:
    """
    Interface to the Neo4j Knowledge Graph for Skills.
    Provides methods to query ontology for transferable skills and career paths.
    """
    def __init__(self, uri: str = "neo4j://localhost:7687", user: str = "neo4j", password: str = "password"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """Closes the Neo4j driver connection."""
        self.driver.close()

    def get_transferable_skills(self, skill: str) -> List[str]:
        """
        Finds skills that are transferable or highly related.
        e.g., Docker -> Kubernetes.
        """
        query = """
        MATCH (s1:Skill {name: $skill})-[:TRANSFERABLE_TO|RELATED_TO*1..2]-(s2:Skill)
        RETURN DISTINCT s2.name as related_skill
        """
        with self.driver.session() as session:
            result = session.run(query, skill=skill)
            return [record["related_skill"] for record in result]
            
    def get_career_paths(self, current_role: str) -> List[str]:
        """
        Identifies potential next roles based on current role in the graph.
        """
        query = """
        MATCH (r1:Role {title: $current_role})-[:PROGRESSES_TO]->(r2:Role)
        RETURN r2.title as next_role
        """
        with self.driver.session() as session:
            result = session.run(query, current_role=current_role)
            return [record["next_role"] for record in result]
