import android.nfc.NfcAdapter;

public class MainActivity {
    private NfcAdapter nfcAdapter;
    public void onCreate() {
        nfcAdapter = NfcAdapter.getDefaultAdapter(this);
    }
}
