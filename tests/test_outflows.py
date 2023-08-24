# import pandas as pd
# import pytest
# from glmpy.outflows import Outflows


# def test_start_date():
#     with pytest.raises(ValueError) as outflows_info:
#         Outflows(
#             start_date='foo',
#             end_date='1997-01-11',
#             base_flow=0.0
#         )
#     assert str(
#         outflows_info.value) == "start_date and end_date must be in valid 'YYYY-MM-DD' format."


# def test_date_order():
#     with pytest.raises(ValueError) as outflows_info:
#         Outflows(
#             start_date='1997-01-11',
#             end_date='1997-01-01',
#             base_flow=0.0
#         )
#     assert str(
#         outflows_info.value) == "start_date must be before end_date."


# def test_negative_base_flow():
#     with pytest.raises(ValueError) as outflows_info:
#         Outflows(
#             start_date='1997-01-01',
#             end_date='1997-01-11',
#             base_flow=-1.0
#         )
#     assert str(
#         outflows_info.value) == "base_flow must be positive."


# def test_empty_outflows_dict():
#     with pytest.raises(ValueError) as outflows_info:
#         Outflows(
#             start_date='1997-01-01',
#             end_date='1997-01-11',
#             base_flow=0.0
#         ).set_discrete_outflows(
#             outflows_dict={}
#         )
#     assert str(
#         outflows_info.value) == "outflows_dict cannot be empty."


# def test_invalid_outflows_dict_keys():
#     with pytest.raises(ValueError) as outflows_info:
#         Outflows(
#             start_date='1997-01-01',
#             end_date='1997-01-11',
#             base_flow=0.0
#         ).set_discrete_outflows(
#             outflows_dict={
#                 "1997/01/02": 1.5,
#                 "1997/01/03": 0.5,
#                 "1997/01/05": 0.5
#             }
#         )
#     assert str(
#         outflows_info.value) == "outflows_dict keys must be in valid 'YYYY-MM-DD' format."


# def test_invalid_outflows_dict_key_prder():
#     with pytest.raises(ValueError) as outflows_info:
#         Outflows(
#             start_date='1997-01-01',
#             end_date='1997-01-11',
#             base_flow=0.0
#         ).set_discrete_outflows(
#             outflows_dict={
#                 "1994-01-02": 1.5,
#                 "1997-01-03": 0.5,
#                 "1997-01-05": 0.5
#             }
#         )
#     assert str(
#         outflows_info.value) == "outflows_dict keys must be between 1997-01-01 and 1997-01-11."


# def test_negative_outflows_dict_values():
#     with pytest.raises(ValueError) as outflows_info:
#         Outflows(
#             start_date='1997-01-01',
#             end_date='1997-01-11',
#             base_flow=0.0
#         ).set_discrete_outflows(
#             outflows_dict={
#                 "1997-01-02": 1.5,
#                 "1997-01-03": -0.5,
#                 "1997-01-05": 0.5
#             }
#         )
#     assert str(
#         outflows_info.value) == "outflows_dict values must be positive."


# def test_overflow_start_date():
#     with pytest.raises(ValueError) as outflows_info:
#         Outflows(
#             start_date='1997-01-01',
#             end_date='1997-01-11',
#             base_flow=0.0
#         ).set_continuous_outflows(
#             outflow_start_date='foo',
#             outflow_end_date='1997-01-11',
#             outflow_volume=1.5
#         )

#     assert str(
#         outflows_info.value) == "outflow_start_date and outflow_end_date must be in valid 'YYYY-MM-DD' format."


# def test_negative_overflow_volume():
#     with pytest.raises(ValueError) as outflows_info:
#         Outflows(
#             start_date='1997-01-01',
#             end_date='1997-01-11',
#             base_flow=0.0
#         ).set_continuous_outflows(
#             outflow_start_date='1997-01-07',
#             outflow_end_date='1997-01-11',
#             outflow_volume=-1.5
#         )

#     assert str(
#         outflows_info.value) == "outflow_volume must be positive."


# def test_overflow_date_order():
#     with pytest.raises(ValueError) as outflows_info:
#         Outflows(
#             start_date='1997-01-01',
#             end_date='1997-01-11',
#             base_flow=0.0
#         ).set_continuous_outflows(
#             outflow_start_date='1997-01-11',
#             outflow_end_date='1997-01-07',
#             outflow_volume=1.5
#         )

#     assert str(
#         outflows_info.value) == "outflow_start_date must be before outflow_end_date."


# def test_overflow_date_range():
#     with pytest.raises(ValueError) as outflows_info:
#         Outflows(
#             start_date='1997-01-01',
#             end_date='1997-01-11',
#             base_flow=0.0
#         ).set_continuous_outflows(
#             outflow_start_date='1997-01-07',
#             outflow_end_date='1997-01-12',
#             outflow_volume=1.5
#         )

#     assert str(
#         outflows_info.value) == "outflow_start_date and outflow_end_date must be within 1997-01-01 and 1997-01-11."


# def test_non_string_file_path():
#     with pytest.raises(ValueError) as outflows_info:
#         Outflows(
#             start_date='1997-01-01',
#             end_date='1997-01-11',
#             base_flow=0.0
#         ).write_outflows(
#             path_to_outflows_csv=1
#         )

#     assert str(
#         outflows_info.value) == "path_to_outflows_csv must be a string."
