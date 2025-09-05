
#!/usr/bin/env sh
# Wrapper shim: if local ./gradle/wrapper/gradle-wrapper.jar exists, use it.
# Otherwise, fallback to system 'gradle' (Termux package).
if [ -f "$(dirname "$0")/gradle/wrapper/gradle-wrapper.jar" ]; then
  DIR="$(cd "$(dirname "$0")" && pwd)"
  exec "$DIR/gradle/wrapper/gradle-wrapper.jar" "$@"
else
  echo "Wrapper JAR missing; using system 'gradle' instead..."
  exec gradle "$@"
fi
