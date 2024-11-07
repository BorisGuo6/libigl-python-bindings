#include "default_types.h"
#include <igl/average_from_edges_onto_vertices.h>
#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>
#include <nanobind/eigen/dense.h>

namespace nb = nanobind;
using namespace nb::literals;

namespace pyigl
{
  nb::object average_from_edges_onto_vertices(
    const nb::DRef<const Eigen::MatrixXI> &F,
    const nb::DRef<const Eigen::MatrixXI> &E,
    const nb::DRef<const Eigen::MatrixXI> &oE,
    const nb::DRef<const Eigen::VectorXN> &uE)
  {
    Eigen::VectorXN uV;
    igl::average_from_edges_onto_vertices(F, E, oE, uE, uV);
    return nb::cast(uV);
  }
}

// Bind the wrapper to the Python module
void bind_average_from_edges_onto_vertices(nb::module_ &m)
{
  m.def(
    "average_from_edges_onto_vertices", 
    &pyigl::average_from_edges_onto_vertices, 
    "F"_a, "E"_a, "oE"_a, "uE"_a,
R"(Move a scalar field defined on edges to vertices by averaging
  
@param[in] F #F by 3 triangle mesh connectivity
@param[in] E #E by 3 mapping from each halfedge to each edge
@param[in] oE #E by 3 orientation as generated by orient_halfedges
@param[in] uE #E by 1 list of scalars
@param[out] uV #V by 1 list of  scalar defined on vertices

\see orient_halfedges)"
    );
}
