package com.carfast.android.ui.components

import android.view.ViewGroup
import androidx.camera.view.PreviewView
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLifecycleOwner
import androidx.compose.ui.viewinterop.AndroidView
import com.carfast.camera.CameraController
import com.carfast.ui.components.CameraView

@Composable
actual fun CameraView(
    controller: CameraController,
    modifier: Modifier,
    onImageCaptured: (ByteArray) -> Unit
) {
    val context = LocalContext.current
    val lifecycleOwner = LocalLifecycleOwner.current
    
    val previewView = remember {
        PreviewView(context).apply {
            layoutParams = ViewGroup.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT
            )
        }
    }

    DisposableEffect(controller) {
        onDispose {
            controller.release()
        }
    }

    AndroidView(
        factory = { previewView },
        modifier = modifier
    )
}
