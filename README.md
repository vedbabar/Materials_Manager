# Material Property Explorer

A desktop GUI tool developed during a software engineering internship at Tata Motors to streamline the process of searching, visualizing, and exporting material property data for Finite Element Analysis (FEA).

---

## Problem Solved

<p>
In many engineering environments, material property data is stored across various spreadsheets and documents. Simulation engineers spend significant time manually searching for this data and reformatting it to be compatible with FEA solvers like Abaqus, Nastran, and FEMFAT. This manual process is not only time-consuming but also prone to error.
</p>

<p>
This tool provides a <strong>centralized, user-friendly interface</strong> to manage and utilize material data efficiently.
</p>

---

## Key Features

<ul>
  <li><strong>Advanced Search & Filter:</strong> Instantly search and filter a comprehensive materials database by mechanical properties such as Young's Modulus, Poisson's Ratio, and Yield Strength.</li>
  <li><strong>Data Visualization:</strong> Automatically generate and display stress-strain curves for any selected material using Matplotlib, providing immediate visual feedback to the engineer.</li>
  <li><strong>Direct FEA Export:</strong> Export material data directly into simulation-ready formats, including:
    <ul>
      <li>Abaqus (<code>.inp</code>)</li>
      <li>Nastran (<code>.bdf</code>)</li>
      <li>FEMFAT (<code>.ffj</code>)</li>
    </ul>
  </li>
  <li><strong>Custom Data Entry:</strong> A simple interface for engineers to add new material data, seamlessly saved to the source Excel files.</li>
  <li><strong>User-Friendly Interface:</strong> A clean and intuitive GUI built with Tkinter, featuring right-click context menus for a streamlined workflow.</li>
</ul>

---

## Technology Stack

<ul>
  <li><strong>Language:</strong> Python</li>
  <li><strong>GUI:</strong> Tkinter</li>
  <li><strong>Data Manipulation:</strong> Pandas</li>
  <li><strong>Data Visualization:</strong> Matplotlib</li>
</ul>

---

## Setup and Installation

<ol>
  <li><strong>Clone the repository:</strong>
    <pre><code>git clone https://github.com/vedbabar/Materials_Manager.git
cd Materials_Manager</code></pre>
  </li>
  <li><strong>Create a virtual environment (recommended):</strong>
    <pre><code>python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`</code></pre>
  </li>
  <li><strong>Install the required dependencies:</strong>
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
  <li><strong>Run the application:</strong>
    <pre><code>python main.py</code></pre>
  </li>
</ol>

---

## Screenshots

<p align="center">
  <img src="link_to_your_screenshot1.png" alt="App Screenshot 1" width="400"/>
  <img src="link_to_your_screenshot2.png" alt="App Screenshot 2" width="400"/>
</p>
