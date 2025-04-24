import SwiftUI
import AVFoundation
import shared

struct IosCameraView: UIViewRepresentable {
    let controller: CameraController
    let onImageCaptured: (Data) -> Void
    
    private let previewLayer = AVCaptureVideoPreviewLayer()
    
    func makeUIView(context: Context) -> UIView {
        let view = UIView()
        previewLayer.session = (controller as! IosCameraController).captureSession
        previewLayer.videoGravity = .resizeAspectFill
        view.layer.addSublayer(previewLayer)
        return view
    }
    
    func updateUIView(_ uiView: UIView, context: Context) {
        previewLayer.frame = uiView.bounds
    }
}

// Composable wrapper
@Composable
actual fun CameraView(
    controller: CameraController,
    modifier: Modifier,
    onImageCaptured: (ByteArray) -> Unit
) {
    IosCameraView(
        controller: controller,
        onImageCaptured: { data in
            // Conversion des données iOS en ByteArray Kotlin
            let byteArray = KotlinByteArray(size: Int32(data.count))
            data.withUnsafeBytes { buffer in
                for (index, byte) in buffer.enumerated() {
                    byteArray.set(index: Int32(index), value: Int8(byte))
                }
            }
            onImageCaptured(byteArray)
        }
    )
}
