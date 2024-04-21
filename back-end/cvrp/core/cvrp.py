import collections
import math
from io import BytesIO

import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans


class CVRP:
    def __init__(
        self,
        raw_bytes_dataset,
        max_student_per_node,
        max_distance_from_node,
        bus_capacity,
    ):
        self.raw_bytes_dataset = raw_bytes_dataset
        self.max_distance_from_node = max_distance_from_node
        self.max_student_per_node = max_student_per_node
        self.bus_capacity = bus_capacity

    def solve(self):
        print("Solving CVRP...")
        try:
            self.dataset_df = pd.read_excel(BytesIO(self.raw_bytes_dataset))
            # print(self.dataset_df.head())
            # print(self.dataset_df)
            cluster_centroids, cluster_labels = self.cluster()
            routes = self.schedule_route()
        except Exception as e:
            print(e)

        finally:
            print("Solve CVRP done!")
            return cluster_centroids, cluster_labels, routes

    def cluster(self):
        try:
            print("####################################")
            print("Start clustering...")
            last_centroid = []
            last_labels = []

            self.dataset = self.dataset_df[["Lat", "Long"]].values.tolist()

            losses = []
            K = len(self.dataset)

            K_optimal = K
            max_demand_for_each_node = self.max_student_per_node
            max_radius = self.max_distance_from_node

            for i in range(1, K):
                # 1.  Huấn luyện với số cụm = i
                kmeans_i = KMeans(n_clusters=i, random_state=0)
                kmeans_i.fit(self.dataset)

                # 2. Tính _hàm biến dạng_
                # 2.1. Khoảng cách tới toàn bộ centroids
                d2centroids = cdist(
                    self.dataset, kmeans_i.cluster_centers_, "euclidean"
                )  # shape (n, k)

                # 2.2. Khoảng cách tới centroid gần nhất
                min_distance = np.min(d2centroids, axis=1)  # shape (n)
                max_distance_any_centroids = max(min_distance)
                frequencies_each_labels = collections.Counter(kmeans_i.labels_)
                most_common_labels = max(
                    frequencies_each_labels, key=frequencies_each_labels.get
                )
                frequency_of_most_common_labels = frequencies_each_labels.get(
                    most_common_labels
                )
                # print('K: ', i)
                # print('Min distance: ', min_distance)
                # print('Labels: ', kmeans_i.labels_)
                # print('Count frequency of each label: ', collections.Counter(kmeans_i.labels_))
                # print('Max freqency: ', frequency_of_most_common_labels)
                # print('Max distance to any centroids', max_distance_any_centroids)

                loss = np.sum(min_distance)
                losses.append(loss)
                if (
                    frequency_of_most_common_labels < max_demand_for_each_node
                    and max_distance_any_centroids < max_radius
                    and K_optimal == K
                ):
                    K_optimal = i
                    print("K optimal: ", i)
                    last_centroid = kmeans_i.cluster_centers_
                    last_labels = kmeans_i.labels_
                    last_frequencies_each_labels = collections.Counter(kmeans_i.labels_)
                    break

            self.cluster_centroids = last_centroid
            self.cluster_labels = last_labels
            self.cluster_frequencies_each_labels = last_frequencies_each_labels

            print("Cluster centroid: ", self.cluster_centroids)
            print("Cluster labels: ", self.cluster_labels)
            print(
                "Cluster frequencies each labels: ",
                self.cluster_frequencies_each_labels,
            )
        except Exception as e:
            print(e)

        finally:
            print("End clustering!")
            print("####################################")
            return last_centroid, last_labels

    def schedule_route(self):
        try:
            routes = {"routes_greedy": [], "routes_saving": []}
            nodes = {}
            for i in range(len(self.cluster_centroids)):
                coord = self.cluster_centroids[i]

                demand = len(np.where(self.cluster_labels == i)[0])

                np.append(coord, demand)

                nodes[i] = {"node": i, "coord": coord, "demand": demand}

            routes_greedy = self.greedy_algo(nodes)
            routes_saving = self.saving_algo(nodes)

            routes["routes_greedy"] = routes_greedy
            routes["routes_saving"] = routes_saving

            print("####################################")
            print("Final routes: ", routes)
            self.routes = routes
        except Exception as e:
            print(e)

        finally:
            return routes

        """
        Schedule using greedy algorithm
        """

    def greedy_algo(self, nodes):
        try:
            print("####################################")
            print("Starting greedy algorithm ...")
            count_bus = 0
            current_pot = [[0, 0]]
            cost = 0

            routes = []

            remaining = True

            capacity = self.bus_capacity

            nodes_df = pd.DataFrame.from_dict(nodes, orient="index")
            node_list = list(nodes_df.node)
            node_coord_list = list(nodes_df.coord)

            while remaining:
                count_bus += 1
                tmp_route = []
                # print("Routing for bus ", count_bus - 1)
                while True:
                    # print(
                    #     "==============================================================="
                    # )
                    if len(node_list) == 0:

                        # Distance from depot to last node of route
                        cost += math.dist([0, 0], current_pot[0])
                        routes.append(tmp_route)
                        print("List route result current: ", routes)

                        cost = 0
                        current_pot = [[0, 0]]
                        capacity = self.bus_capacity
                        remaining = len(node_list)
                        break
                    # print("Remain node: ", node_list)

                    next_index = np.argmin(cdist(current_pot, node_coord_list))
                    next_pot = node_list[next_index]

                    # print("Next pot: ", next_pot)
                    # print("Demand for next pot: ", nodes_df.demand[next_pot])
                    # print("Capacity remain: ", capacity)
                    if capacity - nodes_df.demand[next_pot] > 0:
                        capacity -= nodes_df.demand[next_pot]
                        # print("Remaining capacity: ", capacity)

                        # print(
                        #     "Current cost: ",
                        #     np.min(cdist(current_pot, node_coord_list)),
                        # )
                        cost += np.min(cdist(current_pot, node_coord_list))

                        current_pot = [node_coord_list[next_index]]

                        tmp_route.append(next_pot)

                        node_list.pop(next_index)
                        node_coord_list.pop(next_index)

                        # print("Cost: ", cost)
                        # print("Remain node: ", node_list)
                        # print("Remain coord: ", node_coord_list)
                        # print("Current route: ", tmp_route)
                        # print("Current pot: ", current_pot)

                    else:

                        # Distance from depot to last node of route
                        cost += math.dist([0, 0], current_pot[0])
                        routes.append(tmp_route)
                        # print("List route result current: ", routes)

                        cost = 0
                        current_pot = [[0, 0]]
                        capacity = self.bus_capacity
                        remaining = len(node_list)
                        break
                # if count_bus > 20:
                #     break

            print("Routes find by using greedy algorithm: ", routes)

        except Exception as e:
            print(e)

        finally:
            print("End greedy algorithm ...")
            print("####################################")
            return routes

        """
        Schedule using Saving Clarke Wright algorithm
        """

    def saving_algo(self, nodes):
        savingAlgoSolver = SavingAlgoSolver(
            cluster_centroids=self.cluster_centroids,
            nodes=nodes,
            bus_capacity=self.bus_capacity,
        )
        routes_saving = savingAlgoSolver.run()

        return routes_saving


class SavingAlgoSolver:
    def __init__(self, cluster_centroids, nodes, bus_capacity):
        self.cluster_centroids = cluster_centroids
        self.nodes = nodes
        self.bus_capacity = bus_capacity

    def get_list_saving(self):
        try:
            savings = dict()

            distance_from_depot = cdist([[0, 0]], self.cluster_centroids)
            number_of_node = len(self.cluster_centroids)

            for i in range(number_of_node):
                for j in range(number_of_node):
                    if i != j:
                        first_node = max(i, j)
                        second_node = min(i, j)

                        key = "(" + str(first_node) + "," + str(second_node) + ")"
                        saving_distance = (
                            distance_from_depot[0][i]
                            + distance_from_depot[0][j]
                            - math.dist(
                                self.cluster_centroids[i], self.cluster_centroids[j]
                            )
                        )
                        savings[key] = saving_distance
        except Exception as e:
            print(e)
        finally:
            return savings

        """
        convert link string to tuple: i.e: str(8,5) to (8,5)
        """

    def get_node(self, link):
        link = link[1:]
        link = link[:-1]

        nodes = link.split(",")
        return [int(nodes[0]), int(nodes[1])]

        """
        determine if a node is interior to a route
        """

    def is_interior(self, node, route):
        check = True
        try:
            i = route.index(node)

            # if node adjacent to depot, it's not interior
            if i == 0 or i == (len(route) - 1):
                check = False
        except:
            check = False

        return check

        """
        merge two routes with connection link
        """

    def merge(self, route1, route2, link):
        if route1.index(link[0]) != (len(route1) - 1):
            route1.reverse()

        if route2.index(link[1]) != 0:
            route2.reverse()

        return route1 + route2

        """
        sum up demand in route
        """

    def sum_demand(self, route, nodes):
        sum = 0

        for node in route:
            sum += nodes.demand[node]

        return sum

        """
        # Determine:
        ## 1. If node in link is in any route in current routes -> count_in > 0 (count_in = 1, mean 1 node in link, 
            count_in = 2, mean both nodes in link in arbitrary route)
        ## 2. Which node in link in any route in current routes -> return into node_in_route
        ## 3. Which route, node belong to in step 2 -> return id of that route to route_id
        ## 4. Check both nodes of link is in the same route -> overlap = 1, yes; otherwise, no
        """

    def which_route(self, link, routes):
        # Initial empty
        node_in_route = []
        route_id = []
        count_in = 0
        overlap = 0

        for route in routes:
            for node in link:
                try:
                    route.index(node)
                    route_id.append(routes.index(route))
                    node_in_route.append(node)
                    count_in += 1
                except:
                    # Node not in route
                    pass

        if count_in == 2 and route_id[0] == route_id[1]:
            overlap = 1

        return node_in_route, count_in, route_id, overlap

    def run(self):
        print("####################################")
        print("Start running Saving algorithm ...")
        try:
            # List route result
            routes = []

            saving_dict = self.get_list_saving()
            savings_df = pd.DataFrame.from_dict(saving_dict, orient="index")
            savings_df.rename(columns={0: "saving_distance"}, inplace=True)
            savings_df.sort_values(
                by=["saving_distance"], ascending=False, inplace=True
            )

            remaining = True

            capacity = self.bus_capacity

            nodes_df = pd.DataFrame.from_dict(self.nodes, orient="index")
            node_list = list(nodes_df.node)
            step = 0

            for link in savings_df.index:
                step += 1

                if remaining:
                    # print('Step: ', step)

                    link = self.get_node(link)

                    list_node_in_route, count_in, list_route_id, overlap = (
                        self.which_route(link, routes)
                    )

                    # condition a. Either, neither i nor j have already been assigned to a route,
                    # ... in which case a new route is initiated including both i and j

                    if count_in == 0:
                        if self.sum_demand(link, nodes_df) <= capacity:
                            routes.append(link)
                            node_list.remove(link[0])
                            node_list.remove(link[1])

                            # print('Link: ', link, ' fulfills criteria a. so it is created as new row!')
                        else:
                            # print('Though link: ', link, ' fulfills criteria a. but it exceeds maximum load')
                            continue

                    # condition b. Or, exactly one of the two nodes (i or j) has already been included
                    # ... in an existing route and that point is not interior to that route
                    # ... (a point is interior to a route if it is not adjacent to the depot  in the order of traversal of nodes),
                    # ... in which case the link (i, j) is added to that same route

                    elif count_in == 1:
                        first_node = list_node_in_route[0]
                        route_id = list_route_id[0]
                        position = routes[route_id].index(first_node)

                        link_tmp = link.copy()
                        link_tmp.remove(first_node)

                        remain_node = link_tmp[0]

                        cond1 = not self.is_interior(first_node, routes[route_id])
                        cond2 = (
                            self.sum_demand(routes[route_id] + [remain_node], nodes_df)
                            <= capacity
                        )

                        if cond1:
                            if cond2:
                                # print('Link ', link, ' fulfills criteria b. so new node is add to route')

                                if position == 0:
                                    routes[route_id].insert(0, remain_node)

                                else:
                                    routes[route_id].append(remain_node)

                                node_list.remove(remain_node)
                            else:
                                # print('Though link: ', link, ' fulfills criteria b. but it exceeds maximum load')
                                continue
                        else:
                            # print('For link: ', link, ', node', first_node, ' is interior to route, ', routes[route_id], ' so skip this step')
                            continue

                    # condition c. Or, both i and j have already been included in two different existing routes
                    # ... and neither point is interior to its route, in which case the two routes are merged.

                    else:
                        if overlap == 0:
                            first_node = list_node_in_route[0]
                            second_node = list_node_in_route[1]

                            route1 = routes[list_route_id[0]]
                            route2 = routes[list_route_id[1]]

                            cond1 = not self.is_interior(first_node, route1)
                            cond2 = not self.is_interior(second_node, route2)
                            cond3 = (
                                self.sum_demand(route1 + route2, nodes_df) <= capacity
                            )

                            if cond1 and cond2:
                                if cond3:
                                    # print('Route1: ', route1)
                                    # print('Route2: ', route2)
                                    route_tmp = self.merge(
                                        route1, route2, list_node_in_route
                                    )

                                    routes.remove(route1)
                                    routes.remove(route2)

                                    routes.append(route_tmp)

                                    try:
                                        node_list.remove(link[0])
                                        node_list.remove(link[1])
                                    except:
                                        # nodes has been removed from node_list
                                        pass

                                    # print('Link: ', link, ' fulfills criteria c., so route ', route1, ' and route ', route2, ' has been merged')

                                else:
                                    # print('Link: ', link, ' fulfills criteria c. but exceeds maximum load')
                                    continue
                            else:
                                # print('Link: ', link, ' has two node from two different route but not fulfill interior criteria')
                                continue
                        else:
                            # print('Link: ', link, ' is already included in route in list routes result')
                            continue

                    # for route in routes:
                    #     print('Route: ', route, ' with load', self.sum_demand(route, nodes_df))

                else:
                    # print('Done')
                    break

                remaining = bool(len(node_list) > 0)

            for node in node_list:
                routes.append([node])

            print("Routes find by Saving algo: ", routes)

        except Exception as e:
            print(e)

        finally:
            print("####################################")
            print("End Saving algorithm!")
            return routes
