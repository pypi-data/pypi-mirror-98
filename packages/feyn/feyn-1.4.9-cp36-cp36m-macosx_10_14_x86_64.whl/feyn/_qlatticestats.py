"""Module for LatticeStateStats class. Imported when qg._get_stats() is called."""
from typing import List, Dict

import sympy
import graphviz

import numpy as np

import feyn

class LatticeStateStats:
    """Object that manages data for many statistics measured in the QLattice simulator."""

    def __init__(self, stats_dict:Dict) -> "LatticeStateStats":
        """
        Arguments:
            stats_dict {Dict} -- The dictionary that lives in Simulator._stats_dict in the QLattice.

        Returns:
            LatticeStateStats -- Handy object that you can query for the generation of graph probabilities.
        """
        from pandas import DataFrame
        self._dat = DataFrame.from_dict(stats_dict)
        self._nparticles = len(self._dat)

    def __repr__(self) -> str:
        return "Tracking {} for {} particles.".format(
            list(self._dat.columns),
            self._nparticles
        )

    def dat_df(self) -> "DataFrame":
        """Return the Pandas DataFrame of statistics tracked."""
        return self._dat

    def query_graph_prob(self, graph:feyn.Graph) -> float:
        """Query this lattice with a graph configuration to find the probability of it generating a graph like specified in the qconf.

        Arguments:
            qconf {Dict[str, int]} -- The query as a graph configuration. Maps the statistics we track to their value.

        Raises:
            ValueError: Query configuration contains references to statistics not tracked.

        Returns:
            float -- The probability of the lattice generating a graph like specified in the qconf.
        """
        qconf = self._graph_to_query(graph)
        return self.query_prob(qconf)

    def query_prob(self, qconf:Dict[str, int]) -> float:
        """Query this lattice with a graph configuration to find the probability of it generating a graph like specified in the qconf.

        Arguments:
            qconf {Dict[str, int]} -- The query as a graph configuration. Maps the statistics we track to their value.

        Raises:
            ValueError: Query configuration contains references to statistics not tracked.

        Returns:
            float -- The probability of the lattice generating a graph like specified in the qconf.
        """
        if not set(qconf.keys()).issubset(self._dat.columns):
            raise ValueError("Query configuration contains references to statistics not tracked.")

        bool_idx = np.full((len(self._dat),), True)
        for stat, val in qconf.items():
            stat_idx = self._dat[stat] == val
            bool_idx = bool_idx & stat_idx

        return bool_idx.sum() / self._nparticles

    @staticmethod
    def _graph_to_query(graph:feyn.Graph) -> Dict[str, int]:
        """Take a graph from feyn and turn it into a query to ask a LatticeStateStats object how likely we are to generate a graph like this.

        Arguments:
            graph {feyn.Graph} -- The graph you want to turn into a query.

        Returns:
            Dict[str, int] -- Your query, the configuration of the input graph described by various statistics.
        """
        ret = {
            "depth": graph.depth,
            "n_edges": graph.edge_count,
            "n_unary": 0,
            "n_binary": 0,
            "n_events": 0
        }
        for interaction in graph:
            ret["n_events"] += 1
            if interaction.spec.startswith("in") or interaction.spec.startswith("out"):
                continue
            if len(interaction.sources) == 2:
                ret["n_binary"] += 1
            else:
                ret["n_unary"] += 1
        return ret

def expr_config(expr) -> Dict[str, int]:
    """Find the number of binary and unary interactions needed in a graph to match the input sympy expression."""
    symlist = _expr_to_symlist(expr)
    n_unary, n_binary = _symlist_to_narities(symlist)
    return {"n_unary": n_unary, "n_binary": n_binary}

def expr_tree(expr):
    return graphviz.Source(sympy.printing.dot.dotprint(expr))

def _expr_to_symlist(expr) -> List:
    """Remove anything that isn't a symbol from the sympy expression tree, but keep the structure."""
    res = []
    # Remove weights and biases
    is_mul = expr.func.__name__ == "Mul"
    is_add = expr.func.__name__ == "Add"
    if len(expr.args) == 2 and (is_mul or is_add):
        one_numb = sum(map(_is_numeric, expr.args)) == 1
        one_symb = sum(map(_is_symbol, expr.args)) == 1
        one_expr = sum(map(_is_subexpr, expr.args)) == 1
        if one_numb and one_symb:
            for subexpr in expr.args:
                if _is_symbol(subexpr):
                    return subexpr
        elif one_numb and one_expr:
            for subexpr in expr.args:
                if _is_subexpr(subexpr):
                    return _expr_to_symlist(subexpr)
    # Other subexpressions
    for subexpr in expr.args:
        if _is_symbol(subexpr):
            res.append(subexpr)
            continue
        if subexpr.args:
            res.append(_expr_to_symlist(subexpr))
    return res

def _symlist_to_narities(sym_or_list:List, n_unary:int=0, n_binary:int=0) -> (int, int):
    """Count interactions in a possibly deep list of symbols."""
    if _is_symbol(sym_or_list):
        return n_unary, n_binary
    symlist = sym_or_list
    # Update counts
    if len(symlist) > 1:
        n_binary += len(symlist) - 1
    if len(symlist) == 1:
        n_unary += 1
    # Explore subtrees
    for sublist in symlist:
        if _is_symbol(sublist):
            continue
        n_unary, n_binary = _symlist_to_narities(sublist, n_unary, n_binary)
    return n_unary, n_binary

def _is_symbol(expr) -> bool:
    return isinstance(expr, sympy.core.Symbol)

def _is_numeric(expr) -> bool:
    return getattr(sympy.sympify(expr), "__module__", None) == sympy.core.numbers.__name__

def _is_subexpr(expr) -> bool:
    return not _is_symbol(expr) and not _is_numeric(expr)
