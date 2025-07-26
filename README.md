# 🏀 NBA Web Scraper: Async Stats & Box Scores (2020–2024)

Scrape NBA season schedules and box scores from [Basketball-Reference.com](https://www.basketball-reference.com) using **async Python**, **Playwright**, and **BeautifulSoup**.  
Inspired by [Dataquest](https://www.dataquest.io)'s project-based learning: real-world scraping, data cleaning, and automation!

---

## 📌 Project Objective

> Build a fully automated NBA data pipeline that:
- Extracts full season **game schedules**
- Collects **box score pages** for every match
- Saves raw HTML files for future parsing and analysis
- Handles network delays and retries using asynchronous scraping

This project is ideal for:
- Aspiring **data analysts** and **data engineers**
- Fans of **NBA analytics**
- Developers wanting to learn **asynchronous web scraping**

---

## 🔧 Tech Stack

| Tool             | Purpose                                      |
|------------------|----------------------------------------------|
| `asyncio`        | Non-blocking scraping logic                  |
| `Playwright`     | Headless browser to load JavaScript content  |
| `BeautifulSoup`  | Extract data from HTML                       |
| `Pandas` *(TBD)* | For future data cleaning and transformation  |
| `os`, `time`     | File handling and wait intervals             |

---

## 📁 Project Structure