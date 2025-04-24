package com.carfast.android.camera

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.hardware.camera2.CameraManager
import android.hardware.camera2.CameraDevice
import android.hardware.camera2.CameraCaptureSession
import android.hardware.camera2.CameraCharacteristics
import android.hardware.camera2.CaptureRequest
import android.media.ImageReader
import android.view.Surface
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.carfast.camera.CameraController
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.suspendCancellableCoroutine
import kotlin.coroutines.resume
import kotlin.coroutines.resumeWithException

class AndroidCameraController(
    private val context: Context
) : CameraController {
    private val cameraManager = context.getSystemService(Context.CAMERA_SERVICE) as CameraManager
    private var cameraDevice: CameraDevice? = null
    private var captureSession: CameraCaptureSession? = null
    private var imageReader: ImageReader? = null

    override val isInitialized = MutableStateFlow(false)
    override val hasPermission = MutableStateFlow(false)

    override suspend fun requestPermission() {
        // Note: Cette méthode nécessite une activité pour être implémentée
        // L'implémentation réelle devrait être faite dans l'Activity
        hasPermission.value = ContextCompat.checkSelfPermission(
            context,
            Manifest.permission.CAMERA
        ) == PackageManager.PERMISSION_GRANTED
    }

    override suspend fun initializeCamera() = suspendCancellableCoroutine { continuation ->
        try {
            val cameraId = findBackCamera()
            
            if (ActivityCompat.checkSelfPermission(context, Manifest.permission.CAMERA) 
                != PackageManager.PERMISSION_GRANTED) {
                continuation.resumeWithException(SecurityException("Permission caméra non accordée"))
                return@suspendCancellableCoroutine
            }

            cameraManager.openCamera(cameraId, object : CameraDevice.StateCallback() {
                override fun onOpened(camera: CameraDevice) {
                    cameraDevice = camera
                    isInitialized.value = true
                    continuation.resume(Unit)
                }

                override fun onDisconnected(camera: CameraDevice) {
                    camera.close()
                    isInitialized.value = false
                }

                override fun onError(camera: CameraDevice, error: Int) {
                    camera.close()
                    isInitialized.value = false
                    continuation.resumeWithException(Exception("Erreur d'initialisation de la caméra: $error"))
                }
            }, null)
        } catch (e: Exception) {
            continuation.resumeWithException(e)
        }
    }

    override suspend fun startPreview() {
        // L'implémentation dépendra de la Surface fournie par l'UI
    }

    override suspend fun stopPreview() {
        captureSession?.close()
        captureSession = null
    }

    override suspend fun captureImage(): ByteArray? {
        // Implémentation de la capture d'image
        return null
    }

    override fun release() {
        stopPreview()
        cameraDevice?.close()
        cameraDevice = null
        imageReader?.close()
        imageReader = null
    }

    private fun findBackCamera(): String {
        return cameraManager.cameraIdList.first { id ->
            val characteristics = cameraManager.getCameraCharacteristics(id)
            val facing = characteristics.get(CameraCharacteristics.LENS_FACING)
            facing == CameraCharacteristics.LENS_FACING_BACK
        }
    }
}
