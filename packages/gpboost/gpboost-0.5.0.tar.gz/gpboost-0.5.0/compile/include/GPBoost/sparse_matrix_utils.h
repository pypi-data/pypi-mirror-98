/*!
* This file is part of GPBoost a C++ library for combining
*	boosting with Gaussian process and mixed effects models
*
* Copyright (c) 2020 Fabio Sigrist. All rights reserved.
*
* Licensed under the Apache License Version 2.0. See LICENSE file in the project root for license information.
*/
#ifndef GPB_SPARSE_MAT_H_
#define GPB_SPARSE_MAT_H_
#include <memory>
#include <GPBoost/type_defs.h>

extern "C" {
#include <cs.h>
}

namespace GPBoost {

	/*!
	* \brief Solve equation system with a dense lower triangular matrix as left-hand side (Lx=b)
	* \param val Values of lower triangular matrix L in column-major format
	* \param ncol Number of columns
	* \param[out] x Right-hand side vector (solution written on input)
	*/
	void L_solve(const double* val, const int ncol, double* x);

	/*!
	* \brief Solve equation system with the transpose of a dense lower triangular matrix as left-hand side (L'x=b)
	* \param val Values of lower triangular matrix L in column-major format
	* \param ncol Number of columns
	* \param[out] x Right-hand side vector (solution written on input)
	*/
	void L_t_solve(const double* val, const int ncol, double* x);

	/*!
	* \brief Solve equation system with a sparse lower triangular matrix as left-hand side (Lx=b)
	* \param val Values of sparse lower triangular matrix L
	* \param row_idx Row indices corresponding to the values ('InnerIndices' in Eigen)
	* \param col_ptr val indexes where each column starts ('OuterStarts' in Eigen)
	* \param ncol Number of columns
	* \param[out] x Right-hand side vector (solution written on input)
	*/
	void sp_L_solve(const double* val, const int* row_idx, const int* col_ptr, const int ncol, double* x);

	/*!
	* \brief Solve equation system with the transpose of a sparse lower triangular matrix as left-hand side: (L'x=b)
	* \param val Values of sparse lower triangular matrix L
	* \param row_idx Row indices corresponding to the values ('InnerIndices' in Eigen)
	* \param col_ptr val indexes where each column starts ('OuterStarts' in Eigen)
	* \param ncol Number of columns
	* \param[out] x Right-hand side vector (solution written on input)
	*/
	void sp_L_t_solve(const double* val, const int* row_idx, const int* col_ptr, const int ncol, double* x);

	/*!
	* \brief Solve equation system with a sparse left-hand side and a sparse right-hand side (Ax=B) using CSparse function cs_spsolve
	* \param A left-hand side
	* \param B right-hand side
	* \param[out] Solution A^(-1)B
	* \param lower true if A is a lower triangular matrix
	*/
	void sp_Lower_sp_RHS_cs_solve(cs* A, cs* B, sp_mat_t& A_inv_B, bool lower = true);

	/*!
	* \brief Solve equation system with a sparse left-hand side and a sparse right-hand side (Ax=B) using CSparse function cs_spsolve
	* \param A left-hand side. Sparse Eigen matrix is column major format
	* \param B right-hand side. Sparse Eigen matrix is column major format
	* \param[out] Solution A^(-1)B
	* \param lower true if A is a lower triangular matrix
	*/
	void eigen_sp_Lower_sp_RHS_cs_solve(sp_mat_t& A, sp_mat_t& B, sp_mat_t& A_inv_B, bool lower = true);

	/*!
	* \brief Solve equation system with a sparse left-hand side and a sparse right-hand side (Ax=B)
	* \param A left-hand side. Sparse Eigen matrix is column major format
	* \param B right-hand side. Sparse Eigen matrix is column major format
	* \param[out] Solution A^(-1)B
	* \param lower true if A is a lower triangular matrix
	*/
	void eigen_sp_Lower_sp_RHS_solve(sp_mat_t& A, sp_mat_t& B, sp_mat_t& A_inv_B, bool lower = true);

	/*!
	* \brief Caclulate L\H =(L^-1H) if sparse matrices are used. Used in 'CalcGradNegMargLikelihoodLAApprox' for non-Gaussian data
	* \param L lower (or upper) triangular matrix (Cholesky factor)
	* \param H Right-hand side matrix H
	* \param LInvH[out] L\H =(L^-1H)
	* \param lower true if L is a lower triangular matrix
	*/
	void CalcLInvH(sp_mat_t& L, sp_mat_t& H, sp_mat_t& LInvH, bool lower = true);

	/*!
	* \brief Caclulate L\H =(L^-1H) if sparse matrices are used. Used in 'CalcGradNegMargLikelihoodLAApprox' for non-Gaussian data
	* \param L lower (or upper) triangular matrix (Cholesky factor)
	* \param H Right-hand side matrix H
	* \param LInvH[out] L\H =(L^-1H)
	* \param lower true if L is a lower triangular matrix
	*/
	void CalcLInvH(sp_mat_t& L, den_mat_t& H, den_mat_t& LInvH, bool lower = true);

	/*!
	* \brief Caclulate L\H =(L^-1H) if dense matrices are used. Used in 'CalcGradNegMargLikelihoodLAApprox' for non-Gaussian data
	* \param L lower (or upper) triangular matrix (Cholesky factor)
	* \param H Right-hand side matrix H
	* \param LInvH[out] L\H =(L^-1H)
	* \param lower true if L is a lower triangular matrix
	*/
	void CalcLInvH(den_mat_t& L, den_mat_t& H, den_mat_t& LInvH, bool lower = true);

	/*!
	* \brief Caclulate L\H =(L^-1H) if dense matrices are used but H is sparse. Used in 'CalcGradNegMargLikelihoodLAApprox' for non-Gaussian data
	* \param L lower (or upper) triangular matrix (Cholesky factor)
	* \param H Right-hand side matrix H
	* \param LInvH[out] L\H =(L^-1H)
	* \param lower true if L is a lower triangular matrix
	*/
	void CalcLInvH(den_mat_t& L, sp_mat_t& H, den_mat_t& LInvH, bool lower = true);

//	/*!
//	* \brief Caclulate L\H =(L^-1H) if sparse matrices are used. Used in 'CalcGradNegMargLikelihoodLAApprox' for non-Gaussian data
//	* \param L lower (or upper) triangular matrix (Cholesky factor)
//	* \param H Right-hand side matrix H
//	* \param LInvH[out] L\H =(L^-1H)
//	* \param lower true if L is a lower triangular matrix
//	*/
//	//template <class T3, typename std::enable_if< std::is_same<sp_mat_t, T3>::value>::type * = nullptr  >
//	void CalcLInvH(sp_mat_t& L, sp_mat_t& H, sp_mat_t& LInvH, bool lower = true) {
//		eigen_sp_Lower_sp_RHS_solve(L, H, LInvH, lower);
//		//TODO: use eigen_sp_Lower_sp_RHS_cs_solve -> faster? (currently this crashes due to Eigen bug, see the definition of sp_Lower_sp_RHS_cs_solve for more details)
//	}
//
//	/*!
//	* \brief Caclulate L\H =(L^-1H) if dense matrices are used. Used in 'CalcGradNegMargLikelihoodLAApprox' for non-Gaussian data
//	* \param L lower (or upper) triangular matrix (Cholesky factor)
//	* \param H Right-hand side matrix H
//	* \param LInvH[out] L\H =(L^-1H)
//	* \param lower true if L is a lower triangular matrix
//	*/
//	//template <class T3, typename std::enable_if< std::is_same<den_mat_t, T3>::value>::type * = nullptr  >
//	void CalcLInvH(den_mat_t& L, den_mat_t& H, den_mat_t& LInvH, bool lower = true) {
//		LInvH = H;
//		int ncols = (int)L.cols();
//#pragma omp parallel for schedule(static)
//		for (int j = 0; j < (int)H.cols(); ++j) {
//			if (lower) {
//				L_solve(L.data(), ncols, LInvH.data() + j * ncols);
//			}
//			else {
//				L_t_solve(L.data(), ncols, LInvH.data() + j * ncols);
//			}
//		}
//	}
//
//	/*!
//	* \brief Caclulate L\H =(L^-1H) if dense matrices are used but H is sparse. Used in 'CalcGradNegMargLikelihoodLAApprox' for non-Gaussian data
//	* \param L lower (or upper) triangular matrix (Cholesky factor)
//	* \param H Right-hand side matrix H
//	* \param LInvH[out] L\H =(L^-1H)
//	* \param lower true if L is a lower triangular matrix
//	*/
//	//template <class T3, typename std::enable_if< std::is_same<den_mat_t, T3>::value>::type * = nullptr  >
//	void CalcLInvH(den_mat_t& L, sp_mat_t& H, den_mat_t& LInvH, bool lower = true) {
//		LInvH = den_mat_t(H);
//		int ncols = (int)L.cols();
//#pragma omp parallel for schedule(static)
//		for (int j = 0; j < (int)H.cols(); ++j) {
//			if (lower) {
//				L_solve(L.data(), ncols, LInvH.data() + j * ncols);
//			}
//			else {
//				L_t_solve(L.data(), ncols, LInvH.data() + j * ncols);
//			}
//		}
//	}

}  // namespace GPBoost

#endif   // GPB_SPARSE_MAT_H_
