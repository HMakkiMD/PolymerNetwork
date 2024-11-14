clc; clear; close all;
tic
system('python itp_excel.py');  #convert itp to excel file

files = dir('loop*.xlsx');
loop = '';
network = '';
if isempty(files)
    disp('No matching file found.');
else
    loop = files(1).name;
    disp(['Matching file found: ' loop]);
    numberStr = regexpi(loop, 'loop(\d+)\.xlsx', 'tokens', 'once');
    
    if ~isempty(numberStr)
        % Construct the new variable 'a'
        network = ['network' numberStr{1} '.xlsx'];
        disp(['New variable a: ' network]);
    else
        disp('No number found in the filename.');
    end
end

filename_input = loop;
filename_output = network;
sheet = 'Bonds_Constraints';
[~, ~, raw] = xlsread(filename_input, sheet);
bonds = str2double(raw);


% Creating the matrix of clusters where each column represent bead number existing in that cluster ----> "histogram-matrix" sheet in the excel output.
ibonds = size(bonds,1);
jbonds = size(bonds,2);

source_nodes = bonds(:,1);
target_nodes = bonds(:,2);

Z = zeros(ibonds,1);
for i = 1:ibonds
   Z(i) = 1;     
end

edge = Z;

G = graph(source_nodes,target_nodes,edge);
%figure(1);h=plot(G,'Layout','force');

bins = conncomp(G);
bins=bins';
max_bins = max(bins); %number of molecule in box
xsa = size(bins); 
all_bead_No = xsa(1);  %number of beads in box

hist1 = [(1:all_bead_No)' bins]; %each bead number for which cluster
hist2 = sortrows(hist1,2); %sort matrix hist1
hist3 = hist2(:,2);
y = hist(hist3,max_bins); %number of the molecule and number of the beads in it
max_y = max(y);
%hist(hist3,max_bins); 

hist_mat = zeros(max_y,max_bins);
for j=1:max_bins
    c=0;
    for i=1:all_bead_No
        if hist2(i,2)==j
            c=c+1;
            hist_mat(c,j)=hist2(i,1);
        end
    end
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% analysis hist_mat matrix........ hist max is the molecule number and the
% bead number in it

r_hm = size(hist_mat,1); % row number of hist_mat matrix
c_hm = size(hist_mat,2); % column number of hist_mat matrix

N_all = all_bead_No;     % number of all beads
N_C = c_hm;              % number of clusters
N_L_C = r_hm;            % number of beads in largest cluster

P_L_C = (N_L_C/N_all) * 100;     % percent of largest cluster


% bead numbers of each cluster

for i=1:c_hm
    clusters(i,1)=i; % cluster number
    clusters(i,2)=nnz(hist_mat(:,i));  % number of beads in each cluster
    clusters(i,3)=(nnz(hist_mat(:,i))/N_all)*100; % percent of bead number in each cluster
end

max_clusters=max(clusters(:,2));
p_max_clusters=max(clusters(:,3));
mean_clusters=mean(clusters(:,2));
p_mean_clusters=(mean_clusters/N_all)*100;

output=[N_all N_C max_clusters p_max_clusters mean_clusters p_mean_clusters];

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% analysis degree of nodes

% find the node numbers of the largest cluster (such as the node numbers of
% longest clusters)

max_clusters = max(clusters(:,2));
%[r_max_histmat,c_max_histmat]=
d=find(clusters(:,2)==max_clusters);
d=d(1);

largest_cluster_nodes=hist_mat(:,d);


% find degree of largest cluster
largest_cluster_degree=degree(G,largest_cluster_nodes);

% largest cluster node number and degree of nodes
largest_cluster_nodes_degree=[largest_cluster_nodes largest_cluster_degree];

% find nodes with 1, 2 and 3 edges
c1=0; c2=0; c3=0;
for i=1:size(largest_cluster_nodes_degree,1)
    if largest_cluster_nodes_degree(i,2)==1
        c1=c1+1;
        L_degree1(c1,1)=largest_cluster_nodes_degree(i,1);
        L_degree1(c1,2)=largest_cluster_nodes_degree(i,2);      
    end
    
    if largest_cluster_nodes_degree(i,2)==2
        c2=c2+1;
        L_degree2(c2,1)=largest_cluster_nodes_degree(i,1);
        L_degree2(c2,2)=largest_cluster_nodes_degree(i,2);      
    end

    if largest_cluster_nodes_degree(i,2)==3
        c3=c3+1;
        L_degree3(c3,1)=largest_cluster_nodes_degree(i,1);
        L_degree3(c3,2)=largest_cluster_nodes_degree(i,2);      
    end
        
end

% difine network index1:
% number of nodes with 1 degree in largest cluster/number of nodes with 3 degree in largest cluster
%cycles8 = allcycles(G, "MaxCycleLength",i, "MinCycleLength",i);

%network_index1=(size(L_degree1,1)/size(L_degree3,1))
return
xlswrite(filename_output,{'network index1'},'output','G1');
%xlswrite(filename_output,network_index1,'output','G2');

xlswrite(filename_output,largest_cluster_nodes_degree,'the longest cluster');


xlswrite(filename_output,L_degree1,'largest cluster degree1');
xlswrite(filename_output,L_degree2,'largest cluster degree2');
%xlswrite(filename_output,L_degree3,'largest cluster degree3');

xlswrite(filename_output,hist_mat,'histogram-matrix');
xlswrite(filename_output,clusters,'clusters with bead number');
xlswrite(filename_output,output,'output','A2:F2');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%    counting total number of primary loops     %%%%%%%%%%%%%%%%%%%%%%
temp = zeros(length(raw),2);
for i = 1:length(raw)*2
    if bonds(i) <= 44400
        temp(i) = ceil(bonds(i) / 148);
    elseif 44401 <= bonds(i) && bonds(i) <= 51960
        temp(i) = ceil((bonds(i)-(44401-2701)) / 9);      
    end    
end

output_file = 'selected_rows.xlsx';
xlswrite(output_file, temp);
system('python find_loops.py'); % file name 'temp_loop.xlsx' shows the number of primary loops along with the molecules numbers that formed the loops

%**************************************************************
               %******** calculating molecular weight ************
               
filename = filename_output;
sheet = 'histogram-matrix';
LC = xlsread(filename,sheet);
LC_bead_No = LC;%(:,1);
Length_LC=size(LC_bead_No,1);
num_cluster = size(LC,2);
[~, ~, raw] = xlsread(filename_input,' atoms ');
atoms = raw;

all_bead_no = str2num(char(atoms(:,1)));
MM=zeros(1,num_cluster);

for m=1:num_cluster
    for k=1:Length_LC
        if LC_bead_No(k,m)~=0
            for i=1:size(atoms,1)

                if all_bead_no(i)==LC_bead_No(k,m)
            
                     if string(atoms(i,5))=={'C2H4F'}
                        MM(m)=MM(m)+28;
                     end
                     if string(atoms(i,5))=={'C2H4E'}
                        MM(m)=MM(m)+28;
                     end                     
                     if string(atoms(i,5))=={'C2H1'}
                        MM(m)=MM(m)+25;
                     end
                     if string(atoms(i,5))=={'C2H2M'}
                        MM(m)=MM(m)+26;
                     end
                     if string(atoms(i,5))=={'C2H2E'}
                        MM(m)=MM(m)+26;
                     end                     
                     if string(atoms(i,5))=={'C3H5'}
                        MM(m)=MM(m)+41;
                     end
                     if string(atoms(i,5))=={'COOC'}
                        MM(m)=MM(m)+59;
                     end
                     if string(atoms(i,5))=={'C2H31'}
                        MM(m)=MM(m)+27;
                     end
                     if string(atoms(i,5))=={'COO1'}
                        MM(m)=MM(m)+44;
                     end
                     if string(atoms(i,5))=={'ROH'}
                        MM(m)=MM(m)+45;
                     end
                     if string(atoms(i,5))=={'1ROH'}
                        MM(m)=MM(m)+44;
                     end                     
                     if string(atoms(i,5))=={'C2H32'}
                        MM(m)=MM(m)+27;
                     end
                     if string(atoms(i,5))=={'COO2'}
                        MM(m)=MM(m)+44;
                     end                     
                     if string(atoms(i,5))=={'C4H9'}
                        MM(m)=MM(m)+57;
                     end
                     if string(atoms(i,5))=={'C2H33'}
                        MM(m)=MM(m)+27;
                     end
                     if string(atoms(i,5))=={'C2H3C'}
                        MM(m)=MM(m)+27;
                     end
                     if string(atoms(i,5))=={'COOH'}
                        MM(m)=MM(m)+45;
                     end
                     if string(atoms(i,5))=={'1COOH'}
                        MM(m)=MM(m)+44;
                     end
                     if string(atoms(i,5))=={'ARM'}
                        MM(m)=MM(m)+45;
                     end
                     if string(atoms(i,5))=={'1ARM'}
                        MM(m)=MM(m)+30;
                     end
                     if string(atoms(i,5))=={'COR1'}||string(atoms(i,5))=={'COR2'}||string(atoms(i,5))=={'COR3'}
                        MM(m)=MM(m)+28;
                     end                           
                end
            end
        end
    end
end
MM = sortrows(MM, 1);
mn = sum(MM)/size(MM,2);
mw = floor(sum(MM.^2)/(sum(MM)));
PDI = mw/mn;
uniqueNumbers = unique(MM);
counts = zeros(size(uniqueNumbers));

for i = 1:length(uniqueNumbers)
    counts(i) = sum(MM == uniqueNumbers(i));
end
mw_distribution = [uniqueNumbers;counts]';
count_per_column = sum(LC > 0);
test=count_per_column/size(all_bead_no,1);
uniqueNumbers = unique(count_per_column);
counts = zeros(size(uniqueNumbers));
sas = [MM;test]';
unique_values = unique(sas(:, 1));

result_matrix = zeros(length(unique_values), 2);

for i = 1:length(unique_values)
    current_value = unique_values(i);
    rows_with_current_value = sas(sas(:, 1) == current_value, :);
    sum_of_second_column = sum(rows_with_current_value(:, 2));
    result_matrix(i, :) = [current_value, sum_of_second_column];
end

largest_cluster_mw = result_matrix(end,1);
second_largest_cluster_mw = 0;
weight_average_RMW = 0;
mw_RMW = 0;

if size(mw_distribution,1)>1
    second_largest_cluster_mw = result_matrix(end-1,1);
    weight_average_RMW = result_matrix(1:end-1, :);
    MM_RMW = MM;
    MM_RMW = sort(MM_RMW, 'ascend')';
    MM_RMW = MM_RMW(1:end-1, :);
    MM_RMW = MM_RMW';
    mw_RMW = floor(sum(MM_RMW.^2)/(sum(MM_RMW)));
end

xlswrite('analysis.xlsx',result_matrix,'Mw');
xlswrite('analysis.xlsx',{'Molecular_weight'},'mw','D1');
xlswrite('analysis.xlsx',mw,'Mw','D2');
xlswrite('analysis.xlsx',{'largest_cluster'},'mw','F1');
xlswrite('analysis.xlsx',largest_cluster_mw,'Mw','F2');
xlswrite('analysis.xlsx',{'second_largest_cluster'},'mw','H1');
xlswrite('analysis.xlsx',second_largest_cluster_mw,'Mw','H2');

xlswrite('analysis.xlsx',weight_average_RMW,'RMW');
xlswrite('analysis.xlsx',{'Molecular_weight_RMW'},'RMW','D1');
xlswrite('analysis.xlsx',mw_RMW,'RMW','D2');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%% free and dangling chains %%%%%%%%%%%%%%%%%%

MM_1=zeros(1,num_cluster);
MR_1=zeros(Length_LC,num_cluster);
for m=1:num_cluster
    for k=1:Length_LC
        if LC_bead_No(k,m)~=0
            for i=1:size(atoms,1)

                if all_bead_no(i)==LC_bead_No(k,m)
                    
                     if string(atoms(i,5))=={'1ROH'}||string(atoms(i,5))=={'1COOH'}
                        MR_1(k,m)=str2num(char(atoms(i,3))); 
                     end            
                     if string(atoms(i,5))=={'C2H4F'}
                        MM_1(m)=MM_1(m)+28;
                     end
                     if string(atoms(i,5))=={'C2H4E'}
                        MM_1(m)=MM_1(m)+28;
                     end                     
                     if string(atoms(i,5))=={'C2H1'}
                        MM_1(m)=MM_1(m)+25;
                     end
                     if string(atoms(i,5))=={'C2H2M'}
                        MM_1(m)=MM_1(m)+26;
                     end
                     if string(atoms(i,5))=={'C2H2E'}
                        MM_1(m)=MM_1(m)+26;
                     end                     
                     if string(atoms(i,5))=={'C3H5'}
                        MM_1(m)=MM_1(m)+41;
                     end
                     if string(atoms(i,5))=={'COOC'}
                        MM_1(m)=MM_1(m)+59;
                     end
                     if string(atoms(i,5))=={'C2H31'}
                        MM_1(m)=MM_1(m)+27;
                     end
                     if string(atoms(i,5))=={'COO1'}
                        MM_1(m)=MM_1(m)+44;
                     end
                     if string(atoms(i,5))=={'ROH'}
                        MM_1(m)=MM_1(m)+45;
                     end
                     if string(atoms(i,5))=={'1ROH'}
                        MM_1(m)=MM_1(m)+44;
                     end                     
                     if string(atoms(i,5))=={'C2H32'}
                        MM_1(m)=MM_1(m)+27;
                     end
                     if string(atoms(i,5))=={'COO2'}
                        MM_1(m)=MM_1(m)+44;
                     end                     
                     if string(atoms(i,5))=={'C4H9'}
                        MM_1(m)=MM_1(m)+57;
                     end
                     if string(atoms(i,5))=={'C2H33'}
                        MM_1(m)=MM_1(m)+27;
                     end
                     if string(atoms(i,5))=={'C2H3C'}
                        MM_1(m)=MM_1(m)+27;
                     end
                     if string(atoms(i,5))=={'COOH'}
                        MM_1(m)=MM_1(m)+45;
                     end
                     if string(atoms(i,5))=={'1COOH'}
                        MM_1(m)=MM_1(m)+44;
                     end
                     if string(atoms(i,5))=={'ARM'}
                        MM_1(m)=MM_1(m)+45;
                     end
                     if string(atoms(i,5))=={'1ARM'}
                        MM_1(m)=MM_1(m)+30;
                     end
                     if string(atoms(i,5))=={'COR1'}||string(atoms(i,5))=={'COR2'}||string(atoms(i,5))=={'COR3'}
                        MM_1(m)=MM_1(m)+28;
                     end                           
                end
            end
        end
    end
end
MM_1 = sortrows(MM_1, 1);
mn = sum(MM_1)/size(MM_1,2);
mw = floor(sum(MM_1.^2)/(sum(MM_1)));
PDI = mw/mn;

uniqueNumbers = unique(MM_1);
counts = zeros(size(uniqueNumbers));

for i = 1:length(uniqueNumbers)
    counts(i) = sum(MM_1 == uniqueNumbers(i));
end
mw_distribution = [uniqueNumbers;counts]';

unreacted_chains=0;
for i=1:length(mw_distribution)
    if mw_distribution(i,1)==5522
        unreacted_chains = mw_distribution(i,2);
    end  
end
unreacted_chains;
 

[m, n] = size(MR_1);
for col = 1:n
    uniqueValues = unique(MR_1(:, col), 'stable'); % Find unique values while preserving order
    cleanedColumn = zeros(m, 1); % Initialize a temporary column
    cleanedColumn(1:numel(uniqueValues)) = uniqueValues; % Store unique values in the temporary column
    MR_1(:, col) = cleanedColumn; % Replace the original column with the cleaned column
end


count = sum(sum(MR_1 > 0, 1) == 1);
reacted_chains_1 = count;

xlswrite('analysis.xlsx',{'unreacted chains'},'ACR_junction','A1');
xlswrite('analysis.xlsx',unreacted_chains,'ACR_junction','A2');
xlswrite('analysis.xlsx',{'reacted_chains_1'},'ACR_junction','C1');
xlswrite('analysis.xlsx',reacted_chains_1,'ACR_junction','C2');

system('python HMMM_HMMM_number.py');
toc