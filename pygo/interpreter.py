from .context import Context
from .general.exceptions import NoVisitMethod, RTException
from .general.number import Number
from .general.token import TokenType
from .rt_result import RTResult
from .tree import BinOpNode, Node, NumberNode, UnaryOpNode, VarAccessNode, VarAssignNode

from typing import Optional


class Interpreter():

    def visit(self, node: Node, context: Context) -> Optional[Number]:
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node: Node, context: Context) -> None:
        raise NoVisitMethod(node)

    def visit_NumberNode(self, node: NumberNode, context: Context) -> RTResult:
        return RTResult().success(
            Number(node.tok.value).set_context(
                context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_VarAssignNode(self, node: VarAssignNode, context: Context) -> RTResult:
        res = RTResult()
        var_name = node.tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.error:
            return res
        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_VarAccessNode(self, node: VarAccessNode, context: Context) -> RTResult:
        res = RTResult()
        var_name = node.tok.value
        value = context.symbol_table.get(var_name)

        if value is None:
            return res.failure(RTException(
                pos_start=node.pos_start,
                pos_end=node.pos_end,
                details=f'"{var_name}" is not defined',
                context=context
            ))

        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)

    def visit_BinOpNode(self, node: BinOpNode, context: Context) -> RTResult:
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error:
            return res
        right = res.register(self.visit(node.right_node, context))
        if res.error:
            return res

        if node.op_tok.token_type == TokenType.PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.token_type == TokenType.MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.token_type == TokenType.MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.token_type == TokenType.DIV:
            result, error = left.divided_by(right)
        elif node.op_tok.token_type == TokenType.POW:
            result, error = left.powed_by(right)

        if error:
            return res.failure(error)

        return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node: UnaryOpNode, context: Context) -> RTResult:
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.error:
            return res

        if node.op_tok.token_type == TokenType.MINUS:
            number, error = number.multed_by(Number(-1))
            if error:
                return res.failure(error)

        return res.success(number.set_pos(node.pos_start, node.pos_end))
