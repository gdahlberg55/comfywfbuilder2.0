#!/usr/bin/env python3
"""
Flux Model Downloader with GUI
Simple interface to download Flux models
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import urllib.request
from pathlib import Path
import webbrowser

class FluxDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Flux Model Downloader")
        self.root.geometry("600x500")
        
        self.models_dir = Path(r"C:\Users\gdahl\Documents\ComfyUI\models")
        
        # Header
        header = tk.Label(root, text="FLUX MODEL DOWNLOADER", font=("Arial", 16, "bold"))
        header.pack(pady=10)
        
        # Info
        info = tk.Label(root, text="Download essential Flux models for ComfyUI\nTotal size: ~12.5 GB", font=("Arial", 10))
        info.pack(pady=5)
        
        # Models list
        self.models = [
            {
                "name": "FLUX UNET Model",
                "file": "flux1-dev-fp8.safetensors",
                "size": "11.9 GB",
                "url": "https://huggingface.co/Comfy-Org/flux1-dev/resolve/main/flux1-dev-fp8_e4m3fn.safetensors",
                "path": self.models_dir / "unet" / "flux1-dev-fp8.safetensors"
            },
            {
                "name": "CLIP-L Text Encoder",
                "file": "clip_l.safetensors",
                "size": "246 MB",
                "url": "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors",
                "path": self.models_dir / "clip" / "clip_l.safetensors"
            },
            {
                "name": "Flux VAE",
                "file": "ae.safetensors",
                "size": "335 MB",
                "url": "https://huggingface.co/black-forest-labs/FLUX.1-dev/resolve/main/ae.safetensors",
                "path": self.models_dir / "vae" / "ae.safetensors"
            }
        ]
        
        # Model status frame
        status_frame = tk.LabelFrame(root, text="Model Status", padx=10, pady=10)
        status_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.status_labels = []
        for i, model in enumerate(self.models):
            frame = tk.Frame(status_frame)
            frame.pack(fill="x", pady=5)
            
            # Check if exists
            exists = model["path"].exists()
            status_text = "[OK] Installed" if exists else "[MISSING]"
            color = "green" if exists else "red"
            
            status = tk.Label(frame, text=status_text, fg=color, width=12)
            status.pack(side="left")
            
            name = tk.Label(frame, text=f"{model['name']} ({model['size']})", anchor="w")
            name.pack(side="left", padx=10)
            
            # Download button for individual model
            btn = tk.Button(frame, text="Download" if not exists else "Re-download",
                          command=lambda m=model: self.download_single(m),
                          state="normal" if not exists else "disabled")
            btn.pack(side="right")
            
            self.status_labels.append((status, btn))
        
        # Progress bar
        self.progress = ttk.Progressbar(root, length=400, mode='determinate')
        self.progress.pack(pady=10)
        
        self.progress_label = tk.Label(root, text="Ready to download")
        self.progress_label.pack()
        
        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        
        self.download_all_btn = tk.Button(button_frame, text="Download All Missing", 
                                         command=self.download_all, bg="green", fg="white",
                                         font=("Arial", 10, "bold"))
        self.download_all_btn.pack(side="left", padx=5)
        
        copy_btn = tk.Button(button_frame, text="Copy Links to Clipboard", 
                           command=self.copy_links)
        copy_btn.pack(side="left", padx=5)
        
        open_folder_btn = tk.Button(button_frame, text="Open Models Folder", 
                                   command=self.open_folder)
        open_folder_btn.pack(side="left", padx=5)
        
        # Status bar
        self.status_bar = tk.Label(root, text="Ready", bd=1, relief="sunken", anchor="w")
        self.status_bar.pack(side="bottom", fill="x")
    
    def download_single(self, model):
        """Download a single model"""
        thread = threading.Thread(target=self._download_worker, args=(model,))
        thread.start()
    
    def download_all(self):
        """Download all missing models"""
        missing = [m for m in self.models if not m["path"].exists()]
        if not missing:
            messagebox.showinfo("Info", "All models are already installed!")
            return
        
        thread = threading.Thread(target=self._download_all_worker, args=(missing,))
        thread.start()
    
    def _download_worker(self, model):
        """Worker thread for downloading"""
        self.download_all_btn.config(state="disabled")
        self.status_bar.config(text=f"Downloading {model['file']}...")
        
        try:
            # Create directory
            model["path"].parent.mkdir(parents=True, exist_ok=True)
            
            def hook(block_num, block_size, total_size):
                downloaded = block_num * block_size
                percent = min(downloaded * 100 / total_size, 100)
                self.progress['value'] = percent
                mb_down = downloaded / 1024 / 1024
                mb_total = total_size / 1024 / 1024
                self.progress_label.config(text=f"{mb_down:.1f} / {mb_total:.1f} MB ({percent:.1f}%)")
            
            urllib.request.urlretrieve(model["url"], model["path"], reporthook=hook)
            
            self.status_bar.config(text=f"Downloaded {model['file']}")
            messagebox.showinfo("Success", f"Downloaded {model['name']}")
            
            # Update status
            self.refresh_status()
            
        except Exception as e:
            self.status_bar.config(text="Download failed")
            messagebox.showerror("Error", f"Failed to download {model['name']}:\n{str(e)}")
        
        finally:
            self.download_all_btn.config(state="normal")
            self.progress['value'] = 0
            self.progress_label.config(text="Ready to download")
    
    def _download_all_worker(self, models):
        """Download multiple models"""
        for model in models:
            self._download_worker(model)
    
    def copy_links(self):
        """Copy download links to clipboard"""
        links = []
        for model in self.models:
            links.append(f"{model['name']}:\n{model['url']}\n")
        
        text = "\n".join(links)
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status_bar.config(text="Links copied to clipboard")
    
    def open_folder(self):
        """Open models folder in explorer"""
        import os
        os.startfile(self.models_dir)
    
    def refresh_status(self):
        """Refresh model status"""
        for i, model in enumerate(self.models):
            exists = model["path"].exists()
            status_text = "[OK] Installed" if exists else "[MISSING]"
            color = "green" if exists else "red"
            self.status_labels[i][0].config(text=status_text, fg=color)
            self.status_labels[i][1].config(state="disabled" if exists else "normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = FluxDownloader(root)
    root.mainloop()