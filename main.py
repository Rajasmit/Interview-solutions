from train_route import TrainRoutes
from simple_util import generateAdjacencyList


def main():
    adjacency_list = generateAdjacencyList("train-graph-1.txt")
    train_routes = TrainRoutes(adjacency_list)

    print("1.  The Total Distance of the route A-B-C:    ",
          train_routes.distPath("A-B-C"))
    print("2.  The Total Distance of the route A-D:      ",
          train_routes.distPath("A-D"))
    print("3.  The Total Distance of the route A-D-C:    ",
          train_routes.distPath("A-D-C"))
    print("4.  The Total Distance of the route A-E-B-C-D:",
          train_routes.distPath("A-E-B-C-D"))
    print("5.  The Total Distance of the route A-E-D:    ",
          train_routes.distPath("A-E-D"))
    print("6.  Total no# of trips starting at C and ending at C with max" +
          " stops of 3:      ",
          train_routes.numDiffPaths('C', 'C', max_stops=3))
    print("7.  The no# of trips starting at A and ending at C with" +
          " exactly 4 stops:     ",
          train_routes.numDiffPaths('A', 'C', min_stops=4, max_stops=4))
    print("8.  length of the shortest route in terms of distance from A" +
          " to C:          ",
          train_routes.shortestPath('A', 'C'))
    print("9.  length of the shortest route in terms of distance from B" +
          " to B:          ",
          train_routes.shortestPath('B', 'B'))
    print("10. The no# of different routes from C to C with a distance of" +
          " less than 30: ",
          train_routes.numDiffPaths('C', 'C', max_dist=30))


if __name__ == "__main__":
    main()
