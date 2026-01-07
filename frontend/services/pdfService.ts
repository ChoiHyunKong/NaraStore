import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';

/**
 * Generates a PDF from a DOM element
 * @param elementId The ID of the HTML element to capture
 * @param fileName The desired filename for the PDF
 */
export const generatePDF = async (elementId: string, fileName: string) => {
    const element = document.getElementById(elementId);
    if (!element) {
        throw new Error(`Element with id '${elementId}' not found`);
    }

    try {
        // 1. Capture the element as a canvas
        const canvas = await html2canvas(element, {
            scale: 2, // Higher scale for better resolution
            useCORS: true, // Handle images if any (though currently we use icons)
            logging: false,
            backgroundColor: '#ffffff'
        });

        // 2. Initialize jsPDF
        const imgData = canvas.toDataURL('image/png');
        const pdf = new jsPDF('p', 'mm', 'a4');

        // 3. Calculate dimensions to fit A4
        const imgWidth = 210; // A4 width in mm
        const pageHeight = 297; // A4 height in mm
        const imgHeight = (canvas.height * imgWidth) / canvas.width;

        let heightLeft = imgHeight;
        let position = 0;

        // 4. Add first page
        pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
        heightLeft -= pageHeight;

        // 5. Add subsequent pages if content is long
        while (heightLeft >= 0) {
            position = heightLeft - imgHeight;
            pdf.addPage();
            pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
            heightLeft -= pageHeight;
        }

        // 6. Save PDF
        pdf.save(`${fileName}.pdf`);
        return true;

    } catch (error) {
        console.error('PDF generation failed:', error);
        throw error;
    }
};
