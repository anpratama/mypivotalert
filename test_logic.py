from pivot_logic import calculate_standard_pivots, check_proximity

def test_pivots():
    # Contoh data: High=100, Low=80, Close=90
    # P = (100 + 80 + 90) / 3 = 90
    # R1 = (90 * 2) - 80 = 100
    # S1 = (90 * 2) - 100 = 80
    high, low, close = 100, 80, 90
    pivots = calculate_standard_pivots(high, low, close)
    
    print("--- Hasil Penghitungan Pivot ---")
    for k, v in pivots.items():
        print(f"{k}: {v}")
    
    assert pivots['P'] == 90
    assert pivots['R1'] == 100
    assert pivots['S1'] == 80
    print("✅ Penghitungan Pivot Benar!")

def test_alerts():
    pivots = {'P': 90, 'R1': 100, 'S1': 80}
    
    # Harga 99.95 mendekati R1 (100) dengan selisih 0.05%
    price = 99.95
    alerts = check_proximity(price, pivots, threshold_percent=0.1)
    
    print("\n--- Hasil Deteksi Alert ---")
    print(f"Harga: {price}, Threshold: 0.1%")
    for a in alerts:
        print(f"Alert terdeteksi: {a['level']} pada harga {a['value']}")
    
    assert len(alerts) == 1
    assert alerts[0]['level'] == 'R1'
    print("✅ Deteksi Alert Benar!")

if __name__ == "__main__":
    test_pivots()
    test_alerts()
