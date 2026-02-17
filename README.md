# BrowserStack Selenium Automation Assignment

This repository contains my solution for the BrowserStack technical assignment.  
The project demonstrates **Selenium automation**, **web scraping**, **API integration**, and **parallel cross-browser execution using BrowserStack**.

---

## 🚀 Overview

The assignment is divided into two main parts:

1. **Web Scraping & Text Processing**
2. **Cross-Browser Automation on BrowserStack**

The solution was first validated locally and then executed at scale on BrowserStack across multiple browsers and devices.

---

## 🧩 Part 1: Web Scraping & Text Processing (`task.py`)

### What this script does:
- Visits **El País** (Spanish news website)
- Navigates to the **Opinion** section
- Scrapes the **first five opinion articles**
- Extracts:
  - Article title (Spanish)
  - Article content (Spanish)
  - Cover image (if available)
- Saves cover images locally
- Translates article titles from **Spanish to English** using **RapidAPI (Rapid Translate Multi Traduction API)**
- Analyzes translated titles to find **repeated words (count > 2)**

### Key concepts demonstrated:
- Selenium WebDriver
- Dynamic web scraping
- File download handling
- API integration
- Text processing and analysis

---

## 🧩 Part 2: Cross-Browser Testing on BrowserStack (`browserstack_run.py`)

### What this script does:
- Executes Selenium automation on BrowserStack using **Remote WebDriver**
- Runs tests in **parallel (5 threads)** across:
  - Chrome (Windows)
  - Firefox (Windows)
  - Safari (macOS)
  - Android (Samsung Galaxy S23)
  - iOS (iPhone 14)
- Opens the El País Opinion page
- Verifies successful page load
- Explicitly marks each session as **PASSED** on BrowserStack

### Key concepts demonstrated:
- Selenium Remote execution
- Parallel test execution
- Real desktop & mobile browsers
- BrowserStack session status reporting

---

## 🗂️ Project Structure

