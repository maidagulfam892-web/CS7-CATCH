import * as ImageManipulator from "expo-image-manipulator";

/** Downscale on-device before upload to keep edge bandwidth low. */
export async function preprocessCapture(uri: string): Promise<string> {
  const result = await ImageManipulator.manipulateAsync(
    uri,
    [{ resize: { width: 1024 } }],
    { compress: 0.8, format: ImageManipulator.SaveFormat.JPEG },
  );
  return result.uri;
}
