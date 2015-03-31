function runTest(resultsFileName, testName)
if exist(resultsFileName, 'file')
  delete(resultsFileName);
end
fileID = fopen(resultsFileName, 'w');

try
  evalin('base', testName);
  fprintf(fileID,'%d', 0);
catch e
  fprintf(fileID,'%d', 1);
  disp(getReport(e));
end
fclose(fileID);
exit();
end
