from . import Graph, StateDescriptor, NDPath, Path
from runstats import Statistics
from pprint import pprint
import json

def update(f_get_state, f_update, x):
	old_state = f_get_state()
	f_update(x)
	return old_state != f_get_state()


statistics = StateDescriptor(
	constructor=lambda: Statistics(),
	updater=lambda x, s: update(s.get_state, s.push, x[6]),
	merger=lambda s1, s2: s1 + s2,
	serializer=lambda s: json.dumps(s.get_state()),
	deserializer=lambda s: Statistics.fromstate(json.loads(s))
)

g1 = Graph(
    state_descriptors={
        'statistics': statistics
    },
    path_extractor=lambda x: {
        'Time': list(x[:3]),
        'Space': list(x[3:6])
    }
)

g2 = Graph(
    state_descriptors={
        'statistics': statistics
    },
    path_extractor=lambda x: {
        'Time': list(x[:3]),
        'Space': list(x[3:6])
    }
)

g1.push([2019, 6, 15, 'a', 'b', 'c', 100])
g2.push([2019, 6, 18, 'x', 'y', 'z', 300])
g2.push([2019, 6, 15, 'x', 'y', 'z', 500])


g1.merge(g2)

edges = g1.edges()
# for edge in edges:
#     print(edge)


# print(g1.get({
#     'Time': [2019, 6, 15],
#     'Space': []
# }))

# f = open('graph.csv', 'w')
# f.write('Source,Target\n')
# for edge in edges:
#     f.write(f'{edge[0]},{edge[1]}\n')

s = g1.serialize()

g3 = Graph(
    state_descriptors={
        'statistics': statistics
    },
    path_extractor=lambda x: {
        'Time': list(x[:3]),
        'Space': list(x[3:6])
    }
)


g3.from_serialization(s)
print(g3.get({
    'Time': [2019, 6, 15],
    'Space': []
}))


g3.subscribe({
    'Time': [2020],
    'Space': []
}, lambda s: print(s.get_state()), 'statistics')

g3.push([2019, 6, 16, 'x', 'y', 'z', 800])
g3.push([2020, 6, 16, 'a', 'b', 'c', 10000000])
