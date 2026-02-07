# Python Spy Virus
⚠️ **Proceed with caution and at your own responsibility**

## Overview

This project demonstrates a **Python-based spy virus** created strictly for **educational purposes**.  
It is designed to collect specific information from an infected machine and send it to a server, where the data is filtered and organized using the machine’s **MAC address**.

> ⚠️ This repository is for **learning and research only**. Misuse may be illegal.

---

## Main Features

The virus performs **four primary tasks**:

1. Camera and Screenshot Capture  
2. Wi-Fi and Password Theft  
3. Keyboard and Mouse Logging  
4. Persistence and Auto-Launch on Startup  

---

## Concept

The virus gathers sensitive information from the target machine along with its **MAC address**, then sends this data to a remote server.  
The server separates and identifies each dataset based on the originating machine’s MAC address.

---

## Feature Breakdown

### 1. Camera and Screenshot Capture

By importing operating system and camera-related libraries, the application can:

- Take pictures
- Record videos
- Capture screenshots
- Record audio

**Limitation:**  
The camera LED light may alert the user. To reduce detection:

- The camera is activated for only a few milliseconds
- One picture is taken per hour, then the camera shuts down

Screenshot capture occurs every **10 seconds** and cannot be detected by the user.

Using a **low-level language (such as C)** could reduce this limitation, but challenges still remain.

---

### 2. Wi-Fi and Password Theft

This feature uses **command-line instructions** to:

- Retrieve saved Wi-Fi networks
- Extract their passwords
- Encode the data
- Send it to the server

---

### 3. Keyboard and Mouse Logger

- **Keylogger:** Records each keystroke and sends the collected data when the user presses **ENTER**
- **Mouse logger:** Tracks mouse clicks to detect:
  - Important file interactions
  - Pre-login applications
  - File paths and metadata  

This information helps understand the user’s system structure.

---

### 4. Persistence and Auto-Launch

The virus copies itself into multiple directories, especially:

- `AppData` (to ensure auto-launch at startup)

**Requirements:**
- Administrator privileges

**Behavior:**

- Disguised as a legitimate application
- Regularly checks if its copies still exist
- Recreates them if deleted
- Can rename its executable to mimic legitimate system processes

It does **not** appear as a visible application or terminal process and is difficult to detect unless each running process is manually inspected.

---

## Additional Dangerous Feature (Optional)

### ARP Poisoning (Network Propagation)

This feature allows the virus to:

- Scan the local network
- Detect other machines
- Spoof the router’s IP address
- Intercept network traffic

In specific cases (e.g. FTP traffic), the virus can send its own infected files instead of legitimate ones, allowing it to spread across the same network.

---

## Limitations

### 1. Language Choice

- Python is a **high-level language**
- Easier to detect by antivirus software
- Mitigation attempts included code obfuscation and virtualization layers
- Tools used: **Nuitka** (alternatively PyInstaller)

### 2. File Size

- Final executable size: **~60 MB**
- Due to Python runtime and dependencies
- Can remain unnoticed if embedded in a large cracked application

### 3. Lack of Resources

- Malware development is illegal
- Limited public documentation and learning resources

---

## Conclusion

This project is created **strictly for educational and research purposes**.

- ⚠️ Use at your **own risk**
- ⚠️ The author is **not responsible for misuse**
- Cleanup (purge) command-line scripts are provided to completely remove the virus and all its copies from the system


- The link for the .exe file: https://drive.google.com/drive/folders/1irKByttLLiAXlHGiy2ElrGF3CRh79CUK?usp=sharing
