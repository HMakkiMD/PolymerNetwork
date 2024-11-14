clc; clear; close all;
tic
% you need to make two separate excel files (or one with two sheets) each consists of bead numbers you want to show with specific color
filename_input ='loop2.xlsx';
sheet = 'Bonds_Constraints';
[~, ~, raw] = xlsread(filename_input, sheet);
bonds = str2double(raw);

% Graph
ibonds = size(bonds, 1);
jbonds = size(bonds, 2);

source_nodes = bonds(:, 1);
target_nodes = bonds(:, 2);

Z = zeros(ibonds, 1);
for i = 1:ibonds
   Z(i) = 1;     
end

edge = Z;

G = graph(source_nodes, target_nodes, edge);
h = plot(G, 'Layout', 'force');

% highlight nodes
pet_nodeIDs=xlsread('material-index.xlsx','ACR');
highlight(h,pet_nodeIDs,'NodeColor','b','MarkerSize',3)

p3hb_nodeIDs=xlsread('material-index.xlsx','HMMM');
highlight(h,p3hb_nodeIDs,'NodeColor','r','MarkerSize',3)
toc
