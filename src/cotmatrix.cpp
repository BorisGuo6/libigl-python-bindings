#include "default_types.h"
#include <igl/cotmatrix.h>
#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>
#include <nanobind/eigen/dense.h>
#include <nanobind/eigen/sparse.h>

namespace nb = nanobind;
using namespace nb::literals;

namespace pyigl
{
  nb::object cotmatrix(
    const nb::DRef<const Eigen::MatrixXN> &V,
    const nb::DRef<const Eigen::MatrixXI> &F,
    const nb::DRef<const Eigen::VectorXI> &I,
    const nb::DRef<const Eigen::VectorXI> &C,
    bool return_M,
    bool return_P)
  {
    const bool poly = I.size() != 0;
    Eigen::SparseMatrixN L,M,P;
    if(poly)
    {
      igl::cotmatrix(V,I,C,L,M,P);
    }else
    {
      igl::cotmatrix(V,F,L);
    }
    if(poly)
    {
      if(return_M && return_P)
      {
        return nb::make_tuple(L,M,P);
      }else if(return_M)
      {
        return nb::make_tuple(L,M);
      }else if(return_P)
      {
        return nb::make_tuple(L,P);
      }
    }else
    {
      if(return_M || return_P)
      {
        throw std::runtime_error("cotmatrix: M and P only available for polygonal meshes");
      }
    }
    return nb::cast(std::move(L));
  }
}

// Bind the wrapper to the Python module
void bind_cotmatrix(nb::module_ &m)
{
  m.def(
    "cotmatrix",
    &pyigl::cotmatrix, 
    "V"_a, 
    "F"_a=Eigen::MatrixXI(), 
    "I"_a=Eigen::VectorXI(), 
    "C"_a=Eigen::VectorXI(), 
    "return_M"_a=false,
    "return_P"_a=false,
R"(Constructs the cotangent stiffness matrix (discrete laplacian) for a given
mesh (V,F).

  @tparam DerivedV  derived type of eigen matrix for V (e.g. derived from
    MatrixXd)
  @tparam DerivedF  derived type of eigen matrix for F (e.g. derived from
    MatrixXi)
  @tparam Scalar  scalar type for eigen sparse matrix (e.g. double)
  @param[in] V  #V by dim list of mesh vertex positions
  @param[in] F  #F by simplex_size list of mesh elements (triangles or tetrahedra)
  @param[out] L  #V by #V cotangent matrix, each row i corresponding to V(i,:)

\see adjacency_matrix

\note This Laplacian uses the convention that diagonal entries are
**minus** the sum of off-diagonal entries. The diagonal entries are
therefore in general negative and the matrix is **negative** semi-definite
(immediately, -L is **positive** semi-definite)

Cotangent Laplacian (and mass matrix) for polygon meshes according to
"Polygon Laplacian Made Simple" [Bunge et al.\ 2020]

@param[in] V  #V by 3 list of mesh vertex positions
@param[in] I  #I vectorized list of polygon corner indices into rows of some matrix V
@param[in] C  #polygons+1 list of cumulative polygon sizes so that C(i+1)-C(i) = size of
    the ith polygon, and so I(C(i)) through I(C(i+1)-1) are the indices of
    the ith polygon
@param[out] L  #V by #V polygon Laplacian made simple matrix
@param[out] M  #V by #V mass matrix
@param[out] P  #V+#polygons by #V prolongation operator)"
    );
}



