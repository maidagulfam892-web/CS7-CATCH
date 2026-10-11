import { Platform } from 'react-native';

const getApiUrl = () => {
  if (Platform.OS === 'web') {
    return "http://127.0.0.1:8000/api/v1";
  }
  // Apne laptop ka local IP yahan fix kar dein mobile ke liye
  return "http://192.168.0.101:8000/api/v1";
};

export const env = {
  apiUrl: process.env.EXPO_PUBLIC_API_URL ?? getApiUrl(),
  apiKey: process.env.EXPO_PUBLIC_API_KEY ?? "dev-api-key",
};