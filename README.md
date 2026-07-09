# readmission_radar
Readmission Radar is a data challenge to determine the readmission rate for a local hospital.

The dataset from Maven Analytics contains 623 inpatient stay records from a small hospital. Each record represents a patient discharge, and includes the patient ID, admission date, and discharge date.

The analytic task is to calculate the hospital's 30 day readmission rate. 

A discharge counts as a 30-day readmission when the same patient is admitted again within 30 days of their discharge date.

Day 30 is included in the readmission window.

Assume that all records in the dataset have had a full 30-day follow-up window.