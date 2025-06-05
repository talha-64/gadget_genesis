function captureDiv() {
  const captureTarget = document.getElementById("captureArea");

  document.querySelectorAll("*").forEach((el) => {
    const styles = getComputedStyle(el);

    if (styles.color.startsWith("oklch")) {
      el.style.color = "#000"; // fallback text color
    }

    if (styles.backgroundColor.startsWith("oklch")) {
      el.style.backgroundColor = "#fff"; // fallback background
    }
  });

  // Capture the div and download as image
  html2canvas(captureTarget)
    .then((canvas) => {
      const imageData = canvas.toDataURL("image/png");

      // Create a link to trigger download
      const link = document.createElement("a");
      link.href = imageData;
      link.download = "order-summary.png";
      link.click();
    })
    .catch((error) => {
      console.error("Error capturing the div:", error);
      alert("Failed to save image. Please try again.");
    });
}
