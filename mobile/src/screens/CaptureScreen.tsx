import { CameraView, useCameraPermissions } from "expo-camera";
import * as Location from "expo-location";
import { useEffect, useRef, useState } from "react";
import {
  ActivityIndicator,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

import { fetchCoupons, predictImage } from "../services/api";
import { registerPushToken } from "../services/notifications";
import { preprocessCapture } from "../services/preprocess";
import type { CouponMatch, PredictResponse } from "../types/api";

export function CaptureScreen() {
  const insets = useSafeAreaInsets();
  const cameraRef = useRef<CameraView>(null);
  const [permission, requestPermission] = useCameraPermissions();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [prediction, setPrediction] = useState<PredictResponse | null>(null);
  const [coupons, setCoupons] = useState<CouponMatch[]>([]);

  useEffect(() => {
    registerPushToken().catch(() => undefined);
  }, []);

  async function onCapture() {
    if (!cameraRef.current) return;
    setBusy(true);
    setError(null);
    try {
      const photo = await cameraRef.current.takePictureAsync({ quality: 0.8 });
      if (!photo?.uri) throw new Error("No photo captured");
      const prepared = await preprocessCapture(photo.uri);
      const result = await predictImage(prepared);
      setPrediction(result);

      const top = result.detections[0];
      const coords = await Location.getCurrentPositionAsync({}).catch(() => null);
      const couponPayload = await fetchCoupons({
        lat: coords?.coords.latitude,
        lng: coords?.coords.longitude,
        category: top?.category,
        product_label: top?.label,
      });
      setCoupons(couponPayload.results);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Capture failed");
    } finally {
      setBusy(false);
    }
  }

  if (!permission) {
    return (
      <View style={[styles.center, { paddingTop: insets.top }]}>
        <ActivityIndicator color="#95D5B2" />
      </View>
    );
  }

  if (!permission.granted) {
    return (
      <View style={[styles.center, styles.pad, { paddingTop: insets.top }]}>
        <Text style={styles.title}>CATCH needs the camera</Text>
        <Text style={styles.muted}>
          Product detection and fabric analysis start from a still frame.
        </Text>
        <Pressable style={styles.button} onPress={requestPermission}>
          <Text style={styles.buttonLabel}>Allow camera</Text>
        </Pressable>
      </View>
    );
  }

  return (
    <View style={styles.root}>
      <CameraView ref={cameraRef} style={styles.camera} facing="back" />
      <View style={[styles.hud, { paddingBottom: insets.bottom + 16 }]}>
        <Text style={styles.brand}>CATCH</Text>
        <Text style={styles.muted}>Scan apparel, then match local coupons.</Text>
        <Pressable
          style={[styles.button, busy && styles.buttonDisabled]}
          onPress={onCapture}
          disabled={busy}
        >
          <Text style={styles.buttonLabel}>{busy ? "Analyzing…" : "Capture"}</Text>
        </Pressable>
        {error ? <Text style={styles.error}>{error}</Text> : null}
        <ScrollView style={styles.results} contentContainerStyle={styles.resultsInner}>
          {prediction ? (
            <Text style={styles.meta}>
              {prediction.model} · {prediction.inference_ms} ms ·{" "}
              {prediction.fabric?.suggested_material ?? "no fabric"}
            </Text>
          ) : null}
          {prediction?.detections.map((det) => (
            <Text key={`${det.label}-${det.box.x1}`} style={styles.row}>
              {det.label} ({det.category}) {Math.round(det.confidence * 100)}%
            </Text>
          ))}
          {coupons.map((coupon) => (
            <View key={coupon.id} style={styles.card}>
              <Text style={styles.cardTitle}>{coupon.title}</Text>
              <Text style={styles.muted}>
                {coupon.retailer} · {coupon.discount} · {coupon.stock_hint}
              </Text>
            </View>
          ))}
        </ScrollView>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: "#081C15" },
  camera: { flex: 1.2 },
  hud: {
    flex: 1,
    backgroundColor: "#081C15",
    paddingHorizontal: 16,
    paddingTop: 12,
    gap: 8,
  },
  brand: { color: "#D8F3DC", fontSize: 22, fontWeight: "700", letterSpacing: 1 },
  title: { color: "#D8F3DC", fontSize: 20, fontWeight: "600", textAlign: "center" },
  muted: { color: "#95D5B2", fontSize: 13 },
  button: {
    backgroundColor: "#2D6A4F",
    borderRadius: 12,
    paddingVertical: 12,
    alignItems: "center",
  },
  buttonDisabled: { opacity: 0.6 },
  buttonLabel: { color: "#D8F3DC", fontWeight: "600", fontSize: 16 },
  error: { color: "#F4A261" },
  results: { flex: 1 },
  resultsInner: { gap: 8, paddingBottom: 24 },
  meta: { color: "#B7E4C7", fontSize: 12 },
  row: { color: "#D8F3DC", fontSize: 14 },
  card: {
    backgroundColor: "#1B4332",
    borderRadius: 10,
    padding: 10,
  },
  cardTitle: { color: "#D8F3DC", fontWeight: "600" },
  center: { flex: 1, backgroundColor: "#081C15", justifyContent: "center", alignItems: "center" },
  pad: { padding: 24, gap: 12 },
});
