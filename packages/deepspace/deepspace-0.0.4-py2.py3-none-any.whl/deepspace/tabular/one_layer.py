import tensorflow as tf
from deephyper.nas.space import AutoKSearchSpace, SpaceFactory
from deephyper.nas.space.node import ConstantNode, VariableNode
from deephyper.nas.space.op.merge import Concatenate
from deephyper.nas.space.op.op1d import Dense


class OneLayerFactory(SpaceFactory):
    def build(self, input_shape, output_shape, regression=True, **kwargs):
        ss = AutoKSearchSpace(input_shape, output_shape, regression=regression)

        if type(input_shape) is list:
            vnodes = []
            for i in range(len(input_shape)):
                vn = self.gen_vnode()
                vnodes.append(vn)
                ss.connect(ss.input_nodes[i], vn)

            cn = ConstantNode()
            cn.set_op(Concatenate(ss, vnodes))

            vn = self.gen_vnode()
            ss.connect(cn, vn)

        else:
            vnode1 = self.gen_vnode()
            ss.connect(ss.input_nodes[0], vnode1)

        return ss

    def gen_vnode(self) -> VariableNode:
        vnode = VariableNode()
        for i in range(1, 11):
            vnode.add_op(Dense(i, tf.nn.relu))
        return vnode


if __name__ == "__main__":
    shapes = dict(input_shape=(10,), output_shape=(1,))
    factory = OneLayerFactory()
    factory.test(**shapes)
    # factory.plot_model(**shapes)
    # factory.plot_space(**shapes)
