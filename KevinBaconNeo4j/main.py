# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from neo4j import GraphDatabase


def print_KB(tx):
    counter = 0
    for record in tx.run(f'MATCH (bacon:Person {{name:"Kevin Bacon"}})-[:ACTED_IN]->(m)<-[:ACTED_IN]-(coActors), '
                         f'(coActors)-[:ACTED_IN]->(m2)<-[:ACTED_IN]-(cocoActors) '
                         f'WHERE NOT (bacon)-[:ACTED_IN]->()<-[:ACTED_IN]-(cocoActors) AND bacon <> cocoActors '
                         f'RETURN DISTINCT cocoActors'):
        print(record["cocoActors"].get("name"))
        counter += 1
    print(f'Total {counter} connections of degree 2.')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    driver = GraphDatabase.driver("neo4j://localhost:7687",
                                  auth=("", ""))
    with driver.session() as session:
        session.execute_read(print_KB)

    driver.close()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
