
import os
import pandas as pd
import zipfile
import tempfile
import io
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

@method_decorator(csrf_exempt, name='dispatch')
class SplitExcelView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        try:
            # Get uploaded file
            excel_file = request.FILES['file']
            column_name = request.POST.get('column')  # column to filter
            excel_name = request.POST.get('excel_name')
            
            if not column_name:
                return JsonResponse({"error": "Please provide 'column' parameter"}, status=400)

            # Read excel
            df = pd.read_excel(excel_file)

            if column_name not in df.columns:
                return JsonResponse({"error": f"Column '{column_name}' not found in Excel"}, status=400)

            # Create a temporary directory for storing files
            with tempfile.TemporaryDirectory() as temp_dir:
                # Split by unique values
                unique_values = df[column_name].dropna().unique()
                created_files = []
                file_paths = []

                for value in unique_values:
                    filtered_df = df[df[column_name] == value]
                    file_name = f"{str(value).replace(' ', '_')}_{excel_name}.xlsx"  
                    file_path = os.path.join(temp_dir, file_name)
                    filtered_df.to_excel(file_path, index=False, engine='openpyxl')
                    created_files.append(file_name)
                    file_paths.append(file_path)

                # Create zip file in memory
                zip_buffer = io.BytesIO()
                
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for file_path in file_paths:
                        zip_file.write(file_path, os.path.basename(file_path))

                # Get zip content
                zip_content = zip_buffer.getvalue()
                zip_buffer.close()

                # Return zip file as download
                zip_filename = f"split_excel_files_{excel_name}.zip"
                response = HttpResponse(zip_content, content_type='application/zip')
                response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
                response['X-File-Count'] = str(len(created_files))
                response['X-File-Names'] = ','.join(created_files)
                
                return response

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


def excel_splitter_home(request):
    """Serve the HTML page for Excel splitter"""
    return render(request, 'excel_splitter.html')
