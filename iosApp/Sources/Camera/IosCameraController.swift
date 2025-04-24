import AVFoundation
import UIKit
import shared

class IosCameraController: CameraController {
    private let captureSession = AVCaptureSession()
    private var captureDevice: AVCaptureDevice?
    private var imageOutput: AVCapturePhotoOutput?
    
    private let _isInitialized = MutableStateFlow(value: false)
    private let _hasPermission = MutableStateFlow(value: false)
    
    var isInitialized: StateFlow<KotlinBoolean> { return _isInitialized }
    var hasPermission: StateFlow<KotlinBoolean> { return _hasPermission }
    
    func requestPermission() async {
        switch AVCaptureDevice.authorizationStatus(for: .video) {
        case .authorized:
            _hasPermission.value = true
        case .notDetermined:
            _hasPermission.value = await AVCaptureDevice.requestAccess(for: .video)
        default:
            _hasPermission.value = false
        }
    }
    
    func initializeCamera() async throws {
        guard let device = AVCaptureDevice.default(.builtInWideAngleCamera, for: .video, position: .back) else {
            throw NSError(domain: "CameraError", code: -1, userInfo: [NSLocalizedDescriptionKey: "Caméra non disponible"])
        }
        
        captureDevice = device
        
        do {
            let input = try AVCaptureDeviceInput(device: device)
            imageOutput = AVCapturePhotoOutput()
            
            if captureSession.canAddInput(input) {
                captureSession.addInput(input)
            }
            
            if let output = imageOutput, captureSession.canAddOutput(output) {
                captureSession.addOutput(output)
            }
            
            _isInitialized.value = true
            
        } catch {
            throw error
        }
    }
    
    func startPreview() async throws {
        guard !captureSession.isRunning else { return }
        captureSession.startRunning()
    }
    
    func stopPreview() async {
        guard captureSession.isRunning else { return }
        captureSession.stopRunning()
    }
    
    func captureImage() async throws -> KotlinByteArray? {
        guard let output = imageOutput else { return nil }
        
        return try await withCheckedThrowingContinuation { continuation in
            let settings = AVCapturePhotoSettings()
            output.capturePhoto(with: settings) { photo, error in
                if let error = error {
                    continuation.resume(throwing: error)
                    return
                }
                
                guard let imageData = photo?.fileDataRepresentation() else {
                    continuation.resume(returning: nil)
                    return
                }
                
                let byteArray = KotlinByteArray(size: Int32(imageData.count))
                imageData.withUnsafeBytes { buffer in
                    for (index, byte) in buffer.enumerated() {
                        byteArray.set(index: Int32(index), value: Int8(byte))
                    }
                }
                
                continuation.resume(returning: byteArray)
            }
        }
    }
    
    func release() {
        captureSession.stopRunning()
        _isInitialized.value = false
    }
}
