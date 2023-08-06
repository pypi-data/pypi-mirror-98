# Curricula

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/e6d63124ef0c4a939f726c1609841978)](https://www.codacy.com/manual/csci104/curricula?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=csci104/curricula&amp;utm_campaign=Badge_Grade)

Curricula is a set of specifications and tools for managing content and grading assignments in a college-level computer science setting.
It is currently being developed by [Noah Kim](https://noahbkim.github.io) for CSCI 104, the most challenging core-track C++ course at USC for CS majors.

## How Does it Work?

Curricula covers the two main aspects of managing assignments for a programming course.

1. **Assignment creation**: Curricula provides a schema for developing assignments per-problem rather than all at once.
   This allows content producers to easily port assignments from previous semesters to the evolving parameters of the current.
   Assignments can then be built up from their components problems, separating each and combining their independent parts into packages for publishing, grading, etc.

2. **Submission grading**: the other function of Curricula is to provide a robust framework for testing all aspects of submitted code.
   This includes checks for things like correctness, time complexity, resources leakage, and even code style, all while facilitating granular configuration.
   These tests are written to a universal output format so that they can be reinterpreted without having to re-run the code. 

## Using Curricula

Curricula can be used by installing the [command line interface](https://github.com/csci104/curricula-shell).
This repository only contains the core functionality. 
