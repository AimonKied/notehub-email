# Notehub Email Sender

Automated tool for sending the latest note from [NoteHub](https://github.com/AimonKied/notehub) via email.

## Features

- 🔍 Automatically finds the newest `.txt` file in the notes directory
- 📧 Sends via email using SMTP (Custom SMTP servers)
- ✅ Interactive confirmation before sending
- 🔒 Secure TLS-encrypted connection
- 🔑 Credential management via `.env` file

## Requirements

- Python 3.6 or higher
- Access to an email account with SMTP

## Installation

1. Clone or download the repository
2. No additional Python packages required (uses standard libraries)

## Configuration

### 1. Create `.env` file

Create a `.env` file in the project directory:

```bash
FROM_EMAIL=your-email@example.com
TO_EMAIL=recipient@example.com
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
EMAIL_PASSWORD=your-password

# Optional: Different username for SMTP login
SMTP_USERNAME=username
```

### 2. Adjust notes directory

The script searches for notes in `../notehub/notes` by default.
Adjust the path in `send_note.py` if needed.

## Usage

### Interactive Mode

```bash
python3 send_note.py
```

The script will:
1. Find the latest note
2. Show a preview
3. Ask for confirmation
4. Send the email

## SMTP Provider Examples

**Gmail:**
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```
*Note: Requires app-specific password when 2FA is enabled*

**Outlook:**
```
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
```

**Custom Server:**
```
SMTP_SERVER=smtp.your-provider.com
SMTP_PORT=587
SMTP_USERNAME=your-username
```

## Files

- `send_note.py` - Main script (interactive mode)
- `.env` - Configuration file (not in Git)

## Security

⚠️ **Important Notes:**

- The `.env` file is in `.gitignore` and will **not** be committed to Git
- Never store passwords directly in code
- Use app-specific passwords for Gmail/Google accounts with 2FA
- SMTP connections are TLS-encrypted

## Troubleshooting

### Authentication Failed
1. Check username and password in `.env`
2. For Gmail: Use app-specific password
3. Some providers require a separate SMTP username (see `SMTP_USERNAME`)

### No Notes Found
- Make sure the notes directory exists
- Check the path in `send_note.py`
- The script searches recursively for `.txt` files

### Connection Issues
- Check SMTP server and port in `.env`
- Verify firewall settings
- For cloud servers: Ensure port 587 is not blocked
