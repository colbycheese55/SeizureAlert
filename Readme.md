## Inspiration
Epilepsy affects approximately 50 million people worldwide, and for some, seizures can be life-threatening (World Health Organization, 2024). While specialized seizure detection hardware exists, it can be expensive and inaccessible. Given that 60% of Americans work computer-based jobs (Department for Professional Employees, 2024), we wanted to create a free, purely software-based solution that enhances safety for those at risk of seizures.

## What It Does
Seizure Shield is a proactive seizure monitoring tool with four key components:
- **Seizure Stimulus Detection** – Monitors the screen for flashing lights or patterns that could trigger photosensitive epilepsy.
- **Seizure Detection** – Uses a webcam to detect physical signs of a seizure.
- **User Alert System** – Displays a popup asking if the user needs help.
- **Emergency Notification** – Sends an alert to pre-set emergency contacts if the user does not respond.

### Seizure Stimulus Detection
Certain visual stimuli, such as flashing lights, can induce seizures in people with photosensitive epilepsy (Epilepsy Society, 2019). Seizure Shield continuously analyzes the user’s screen, detecting rapid changes in brightness and patterns. If a potential trigger is identified, an alert is triggered.

### Seizure Detection
By utilizing a webcam feed, Seizure Shield monitors for physical seizure symptoms. If abnormal movements are detected, the system activates an alert.

### Alert System & Emergency Notifications
If a seizure or seizure-inducing stimulus is detected, the system displays a popup alert, asking if the user needs assistance. If the user does not dismiss the alert within 10 seconds, Seizure Shield automatically sends a text message to their emergency contact.

## How We Built It
- **Seizure Stimulus Detection**: We used the Python library `mss` to capture rapid screenshots and applied a Fast Fourier Transform (FFT) to analyze frequency changes. By calculating rolling variance, we determined if seizure-inducing patterns were present.
- **Seizure Detection**: Using OpenCV, we processed webcam footage to detect abnormal movement patterns.
- **User Alerts & Emergency Notifications**: A browser-based alert system was implemented to prompt user response before escalating to emergency contacts.

## Challenges We Faced
Developing reliable seizure detection algorithms was our biggest challenge. Ensuring accurate alerts while minimizing false positives required extensive calibration and fine-tuning.

## Accomplishments We’re Proud Of
We’re proud to have built an open-source project that has the potential to save lives by providing accessible seizure monitoring.

## What We Learned
This project deepened our understanding of image processing, real-time monitoring, and algorithm calibration.

## What’s Next for Seizure Shield
Future improvements include refining detection algorithms to further reduce false positives and negatives, as well as expanding compatibility with additional assistive technologies.


## References
Epilepsy Society. (2019, September). Photosensitive epilepsy | Epilepsy Society. Epilepsysociety.org.uk. https://epilepsysociety.org.uk/about-epilepsy/epileptic-seizures/seizure-triggers/photosensitive-epilepsy

How Serious Are Seizures? (2024). Epilepsy Foundation. https://www.epilepsy.com/what-is-epilepsy/understanding-seizures/how-serious-are-seizures#What-is-the-risk-of-seizure-emergencies?

World Health Organization. (2024). Epilepsy. World Health Organization. https://www.who.int/news-room/fact-sheets/detail/epilepsy

The Professional and Technical Workforce: By the Numbers. (2024) Department for Professional Employees AFLCIO. https://www.dpeaflcio.org/factsheets/the-professional-and-technical-workforce-by-the-numbers