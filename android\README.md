# EVE AI Android App

## Build Instructions

### Prerequisites:
- Android Studio (or Gradle + JDK)
- Android SDK

### Build:

1. Open Android Studio
2. File -> Open -> Select `eve/android` folder
3. Wait for Gradle sync
4. Build -> Build APK

### Or via command line:

```bash
cd eve/android
./gradlew assembleDebug
```

The APK will be at: `eve/android/app/build/outputs/apk/debug/app-debug.apk`

### Note:
The app loads from `http://localhost:8000`. For production:
1. Deploy the Python backend to a server
2. Update the URL in MainActivity.kt
