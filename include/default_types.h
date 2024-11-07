#include <Eigen/Dense>
#include <Eigen/Sparse>
#include <cstdint>

///////////////////////////////////////////////////////////////////////////////////
/// Default numeric and integer types. Passing anything else will result in an
/// implicit copy. Developers insisting on native executation of libigl on
/// single-precision (largely untested and possibly error prone) can change this
/// to float and recompile bindings at their own delight or peril.
///////////////////////////////////////////////////////////////////////////////////
using Numeric = double;
using Integer = int64_t;
namespace Eigen
{
  typedef Matrix<Numeric, Dynamic, Dynamic> MatrixXN;
  typedef Matrix<Integer, Dynamic, Dynamic> MatrixXI;
  typedef Matrix<Numeric, Dynamic, 1> VectorXN;
  typedef Matrix<Integer, Dynamic, 1> VectorXI;
  typedef Matrix<Numeric, 1, Dynamic> RowVectorXN;
  typedef Matrix<Integer, 1, Dynamic> RowVectorXI;
  typedef SparseMatrix<Numeric> SparseMatrixN;
  typedef SparseMatrix<Integer> SparseMatrixI;
}


