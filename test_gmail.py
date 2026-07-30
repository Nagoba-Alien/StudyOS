from app.exporters.gmail import GmailExporter

exporter = GmailExporter()

exporter.export(
    sender="nagoba.alien@gmail.com",
    recipient="nagoba.alien@gmail.com",
    subject="StudyOS Gmail Test",
    body="If you're reading this, Gmail API integration works!",
)
