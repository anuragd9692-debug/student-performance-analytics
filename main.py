"""
Student Performance Analytics System
Technologies: Python, NumPy, Pandas
Run: python main.py
"""

import numpy as np
import pandas as pd
from pathlib import Path

DATA_FILE = Path(__file__).parent / "students.csv"


def assign_grade(average):
    """Return a grade based on the student's average marks."""
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 40:
        return "D"
    return "F"


def analyze_students(data):
    """Calculate totals, averages, grades, and pass/fail status."""
    subjects = ["Python", "Mathematics", "English"]
    data = data.copy()

    # NumPy is used for numerical calculations.
    marks_array = data[subjects].to_numpy(dtype=float)
    data["Total"] = np.sum(marks_array, axis=1)
    data["Average"] = np.round(np.mean(marks_array, axis=1), 2)

    grades = []
    results = []
    for _, student in data.iterrows():
        grades.append(assign_grade(student["Average"]))
        # A student passes only when every subject mark is at least 35.
        results.append("Pass" if all(student[subject] >= 35 for subject in subjects) else "Fail")

    data["Grade"] = grades
    data["Result"] = results
    return data


def show_report(data):
    subjects = ["Python", "Mathematics", "English"]
    analyzed = analyze_students(data)

    print("\n" + "=" * 64)
    print("       STUDENT PERFORMANCE ANALYTICS SYSTEM")
    print("=" * 64)
    print("\nSTUDENT SUMMARY")
    print(analyzed[["Student_ID", "Name", "Department", "Total", "Average", "Grade", "Result"]].to_string(index=False))

    print("\nCLASS SUMMARY")
    print(f"Number of students : {len(analyzed)}")
    print(f"Class average      : {analyzed['Average'].mean():.2f}")
    print(f"Highest average    : {analyzed['Average'].max():.2f}")
    print(f"Lowest average     : {analyzed['Average'].min():.2f}")
    print(f"Students passed    : {(analyzed['Result'] == 'Pass').sum()}")
    print(f"Students failed    : {(analyzed['Result'] == 'Fail').sum()}")

    top_average = analyzed["Average"].max()
    top_students = analyzed.loc[analyzed["Average"] == top_average, "Name"].tolist()
    print("Top performer(s)   : " + ", ".join(top_students))

    print("\nSUBJECT-WISE AVERAGES")
    for subject in subjects:
        print(f"{subject:16}: {analyzed[subject].mean():.2f}")

    print("\nATTENDANCE SUMMARY")
    print(f"Class attendance average: {analyzed['Attendance'].mean():.2f}%")
    low_attendance = analyzed.loc[analyzed["Attendance"] < 75, ["Name", "Attendance"]]
    if low_attendance.empty:
        print("No students below 75% attendance.")
    else:
        print(low_attendance.to_string(index=False))

    # Save the analysis to a separate CSV for easy review.
    output_file = Path(__file__).parent / "analysis_results.csv"
    analyzed.to_csv(output_file, index=False)
    print(f"\nDetailed results saved to: {output_file.name}")


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")
    students = pd.read_csv(DATA_FILE)

    required_columns = [
        "Student_ID", "Name", "Department", "Python",
        "Mathematics", "English", "Attendance"
    ]
    missing = [column for column in required_columns if column not in students.columns]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")

    print(f"Loaded {len(students)} student records from {DATA_FILE.name}.")
    show_report(students)


if __name__ == "__main__":
    main()
