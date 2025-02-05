# 🎟️ Automated Ticket Verification and Entry System for Movie Theatres 🎥

## 📌 Abstract
This project aims to enhance the movie theatre experience by automating the ticket verification and entry process. Our system enables patrons to scan their tickets at the entrance, automatically validating them and allowing entry. The system tracks occupancy levels, automatically closing the door when ticket limits are reached. A similar mechanism is used at the exit, providing controlled re-entry and efficient exit management.

For administrators, the system provides detailed insights, including employee records, ticket sales, and scanned entry/exit logs. This ensures smooth operations and enhances security. 🎯

## ✨ Features
- **🎫 Automated Ticket Scanning**: QR code-based validation for seamless entry.
- **👥 Occupancy Management**: Monitors the number of people entering and exiting.
- **📊 Admin Dashboard**: Provides oversight of theatre operations.
- **🚪 Exit and Re-entry Mechanism**: Allows timed exit windows and controlled re-entry.

## 🛠️ Technologies Used
### 💻 Software Requirements
- **🐍 Python** (Programming Language)
- **🖥️ VS Code** (Preferred IDE)

### 📚 Libraries Used
- **🔍 OpenCV**: QR code recognition.
- **📏 Mediapipe**: Person counting for occupancy tracking.
- **🎨 Tkinter & CustomTkinter**: GUI development.
- **🛢️ MySQL Connector**: Database connection.
- **🖼️ Pillow**: Image processing.

## 🖥️ System Requirements
- 🎥 A webcam
- 💾 A computer with at least an Intel i5 processor
- 🎮 A dedicated graphics card (optional for better performance)

## 🚀 Project Plan & Development Stages
1. **📷 QR Recognition Module**: Scans and validates QR-coded tickets.
2. **🔢 Person Counter Development**: Tracks the number of people entering/exiting.
3. **🖥️ GUI Development**: Provides an interactive interface for users.
4. **🔗 Integration and Testing**: Ensures seamless communication between modules.
5. **📂 Admin Panel Creation**: Offers insights into theatre operations.

## 🔧 Setup Instructions
1. Clone the repository:
   ```sh
   git clone https://github.com/Madan2248c/Automated-Ticket-Vrification-and-entry-system-for-theatres
   ```
2. Navigate to the project directory:
   ```sh
   cd automated-ticket-verification
   ```
3. Install dependencies:
   ```sh
   pip install opencv-python mediapipe mysql-connector-python pillow customtkinter
   ```
4. Run the application:
   ```sh
   python main.py
   ```

## 🎯 Summary
This project revolutionizes the ticketing process in movie theatres by automating verification, improving security, and enhancing the customer experience. Our system ensures seamless entry, controlled exits, and efficient theatre management. 🎬
