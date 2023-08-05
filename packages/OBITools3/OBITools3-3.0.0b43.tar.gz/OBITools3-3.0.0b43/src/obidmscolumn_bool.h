/****************************************************************************
 * OBIDMS_column_bool header file                                            *
 ****************************************************************************/

/**
 * @file obidsmcolumn_bool.h
 * @author Celine Mercier
 * @date August 10th 2015
 * @brief Header file for the functions handling OBIColumns containing data with the OBIType OBI_BOOL.
 */


#ifndef OBIDMSCOLUMN_BOOL_H_
#define OBIDMSCOLUMN_BOOL_H_


#include <stdlib.h>
#include <stdio.h>

#include "obidmscolumn.h"
#include "obitypes.h"


/**
 * @brief Sets a value in an OBIDMS column containing data with the type OBI_BOOL, using the index of the element in the line.
 *
 * @warning Pointers returned by obi_open_column() don't allow writing.
 *
 * @param column A pointer as returned by obi_create_column() or obi_clone_column().
 * @param line_nb The number of the line where the value should be set.
 * @param element_idx The index of the element that should be set in the line.
 * @param value The value that should be set.
 *
 * @returns An integer value indicating the success of the operation.
 * @retval 0 on success.
 * @retval -1 if an error occurred.
 *
 * @since July 2015
 * @author Celine Mercier (celine.mercier@metabarcoding.org)
 */
int obi_column_set_obibool_with_elt_idx(OBIDMS_column_p column, index_t line_nb, index_t element_idx, obibool_t value);


/**
 * @brief Recovers a value in an OBIDMS column containing data with the type OBI_BOOL.
 *
 * @param column A pointer as returned by obi_create_column().
 * @param line_nb The number of the line where the value should be recovered.
 * @param element_idx The index of the element that should be recovered in the line.
 *
 * @returns The recovered value.
 * @retval OBIBool_NA the NA value of the type if an error occurred and obi_errno is set.
 *
 * @since July 2015
 * @author Celine Mercier (celine.mercier@metabarcoding.org)
 */
obibool_t obi_column_get_obibool_with_elt_idx(OBIDMS_column_p column, index_t line_nb, index_t element_idx);


/**
 * @brief Sets a value in an OBIDMS column containing data with the type OBI_BOOL,
 *        using the name of the element in the line.
 *
 * @warning Pointers returned by obi_open_column() don't allow writing.
 *
 * @param column A pointer as returned by obi_create_column() or obi_clone_column().
 * @param line_nb The number of the line where the value should be set.
 * @param element_name The name of the element that should be set in the line.
 * @param value The value that should be set.
 *
 * @returns An integer value indicating the success of the operation.
 * @retval 0 on success.
 * @retval -1 if an error occurred.
 *
 * @since August 2015
 * @author Celine Mercier (celine.mercier@metabarcoding.org)
 */
int obi_column_set_obibool_with_elt_name(OBIDMS_column_p column, index_t line_nb, const char* element_name, obibool_t value);


/**
 * @brief Recovers a value in an OBIDMS column containing data with the type OBI_BOOL,
 *        using the name of the element in the line.
 *
 * @param column A pointer as returned by obi_create_column() or obi_clone_column().
 * @param line_nb The number of the line where the value should be recovered.
 * @param element_name The name of the element that should be recovered in the line.
 *
 * @returns The recovered value.
 * @retval OBIBool_NA the NA value of the type if an error occurred and obi_errno is set.
 *
 * @since August 2015
 * @author Celine Mercier (celine.mercier@metabarcoding.org)
 */
obibool_t obi_column_get_obibool_with_elt_name(OBIDMS_column_p column, index_t line_nb, const char* element_name);


#endif /* OBIDMSCOLUMN_BOOL_H_ */

