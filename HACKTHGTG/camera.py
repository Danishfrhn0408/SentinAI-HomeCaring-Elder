import cv2
import requests
import datetime
import time

# ==========================================
# AMARAN: TUKAR URL INI KEPADA URL CLOUD RUN AWAK!
# ==========================================
CLOUD_RUN_URL = "https://sentinai-backend-137181402202.asia-southeast1.run.app/api/emergency-alert"
def mulakan_video_cctv():
    print("Memuatkan video CCTV SentinAI...")
    
    # Tukar kepada nama fail video awak
    nama_fail_video = 'demo_jatuh.mp4' 
    cap = cv2.VideoCapture(nama_fail_video)

    if not cap.isOpened():
        print(f"Ralat: Tidak dapat membuka fail {nama_fail_video}. Pastikan nama betul dan berada dalam folder yang sama.")
        return

    print("\n--- SISTEM VISI SENTINAI (MOD VIDEO) SEDIA ---")
    print("Tekan butang 'j' bila babak jatuh dimainkan untuk HANTAR SIMULASI JATUH.")
    print("Tekan butang 'q' untuk TUTUP sistem.\n")

    while True:
        ret, frame = cap.read()
        
        # Jika video habis, kita ulang (loop) balik dari awal macam CCTV
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        # Tulis arahan pada skrin
        cv2.putText(frame, "SentinAI Vision (CCTV Playback)", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Tekan 'j' untuk kesan jatuh", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        cv2.imshow('Kamera SentinAI', frame)

        # Tunggu 30ms supaya video main pada kelajuan normal (bukan laju sangat)
        key = cv2.waitKey(30) & 0xFF

        if key == ord('j'):
            print("\n[!] PERGERAKAN JATUH DIKESAN! Menghantar data ke Cloud Run...")
            
            payload = {
                "event_type": "fall_detected",
                "confidence": 0.96,
                "timestamp": datetime.datetime.now().isoformat() + "Z"
            }
            
            try:
                response = requests.post(CLOUD_RUN_URL, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    print("\n✅ RESPON DARI GEMINI AI:")
                    print(f"Status: {data.get('status')}")
                    print(f"Tindakan: {data.get('gemini_action')}")
                else:
                    print(f"Ralat Server: {response.status_code}")
            except Exception as e:
                print(f"Gagal menyambung ke Cloud Run. Sila periksa CLOUD_RUN_URL.")

        elif key == ord('q'):
            print("Menutup sistem visi...")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    mulakan_video_cctv()