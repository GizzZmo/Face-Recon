import CoreNFC

func scanNFC() {
    let session = NFCNDEFReaderSession(delegate: self, queue: nil, invalidateAfterFirstRead: true)
    session.begin()
}
