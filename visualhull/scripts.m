clear all
imageKK = cell(23,1);
imageRT = cell(23,1);
viewport = zeros(23,2);
texturename = cell(23,1);
value = jsondecode(fileread('/Users/yuminggu/Desktop/vgl_project/lightstage-mingminghe/owen/cameras.sfm'));
multiview_frame = '/Users/yuminggu/Desktop/vgl_project/lightstage-mingminghe/sihou2/';
for i = 1:9
    view_info = value.views{i};
    viewId = str2num(view_info.viewId);
    poseId = str2num(view_info.poseId);
    intrinsicId = str2num(view_info.intrinsicId);
    calib_img = view_info.path;
    s = strsplit(calib_img,'\');
    image = imread([multiview_frame s{end}]);
    %image = rgb2gray(image);
    silhouettes(:,:,i) = image(:,:)>200;
    KK_info = value.intrinsics(intrinsicId +1);
    KK= [str2num(KK_info.pxFocalLength) 0 str2num(KK_info.principalPoint{1});...
        0  str2num(KK_info.pxFocalLength) str2num(KK_info.principalPoint{2});...
        0 0 1];
    fc = [KK(1,1) KK(2,2)];
    cc = [KK(1,3) KK(2,3)];
    kc=(str2num(KK_info.distortionParams{1}));
    
    Rt_info = value.poses(poseId +1);
    R_temp = Rt_info.pose.transform.rotation
    R = [str2num(R_temp{1}) str2num(R_temp{2}) str2num(R_temp{3}); ...
        str2num(R_temp{4}) str2num(R_temp{5}) str2num(R_temp{6}); ...
        str2num(R_temp{7}) str2num(R_temp{8}) str2num(R_temp{9});];
    t = [ str2num(Rt_info.pose.transform.center{1})  str2num(Rt_info.pose.transform.center{2}) str2num(Rt_info.pose.transform.center{3})];
    
    
    imageRT{i} = [inv(R) -inv(R)*t'];
   
    proj =[inv(R) -inv(R)*t'];
    R =proj(1:3,1:3);
    t = proj(:,4);
    M(:,:,i) = KK*[R t];
end
for j = 1:16
    view_info = value.views{j+9};
    viewId = str2num(view_info.viewId);
    poseId = str2num(view_info.poseId);
    intrinsicId = str2num(view_info.intrinsicId);
    calib_img = view_info.path;
    s = strsplit(calib_img,'\');
    image = imread([multiview_frame s{end}]);
    silhouettes2(:,:,j) = image(:,:)>200;
    KK_info = value.intrinsics(intrinsicId +1);
    KK = [str2num(KK_info.pxFocalLength) 0 str2num(KK_info.principalPoint{1});...
        0  str2num(KK_info.pxFocalLength) str2num(KK_info.principalPoint{2});...
        0 0 1];
    fc = [KK(1,1) KK(2,2)];
    cc = [KK(1,3) KK(2,3)];
    kc=(str2num(KK_info.distortionParams{1}));
    
    Rt_info = value.poses(poseId +1);
    R_temp = Rt_info.pose.transform.rotation
    R = [str2num(R_temp{1}) str2num(R_temp{2}) str2num(R_temp{3}); ...
        str2num(R_temp{4}) str2num(R_temp{5}) str2num(R_temp{6}); ...
        str2num(R_temp{7}) str2num(R_temp{8}) str2num(R_temp{9});];
    t = [str2num(Rt_info.pose.transform.center{1})  str2num(Rt_info.pose.transform.center{2}) str2num(Rt_info.pose.transform.center{3})];
    
    
    imageRT{i} = [inv(R) -inv(R)*t'];
   
    proj =[inv(R) -inv(R)*t'];
    R =proj(1:3,1:3);
    t = proj(:,4);
    M2(:,:,i) = KK*[R t];
    end
%% 4 create voxel grid
voxel_size = [0.25 0.25 0.25];
file_base2 ='other';
switch file_base2
    case 'dinoSR'
        % dinoSR bounding box
        xlim = [-0.07 0.02];
        ylim = [-0.02 0.07];
        zlim = [-0.07 0.02];
    case 'dinoR'
        % dinoR bounding box
        xlim = [-0.03 0.06];
        ylim = [0.022 0.11];
        zlim = [-0.02 0.06];

    case 'templeSR'
        % templeSR bounding box
        xlim = [-0.08 0.03];
        ylim = [0.0 0.18];
        zlim = [-0.02 0.06];

    case 'templeR'
        % templeR bounding box
        xlim = [-0.05 0.11];
        ylim = [-0.04 0.15];
        zlim = [-0.1 0.06];
        
    otherwise
        xlim = [-0.08 0.11];
        ylim = [-0.03 0.18];
        zlim = [-0.1 0.06];
end

[voxels, voxel3Dx, voxel3Dy, voxel3Dz, voxels_number] = InitializeVoxels(xlim, ylim, zlim, voxel_size);


%% 5 project voxel to silhouette
display_projected_voxels = 1;
[voxels_voted] = CreateVisualHull(silhouettes, voxels, M, display_projected_voxels);
%[voxels_voted] = CreateVisualHull2(silhouettes, voxels, M, display_projected_voxels, silhouettes2, M2);

% % display voxel grid
 voxels_voted1 = (reshape(voxels_voted(:,4), size(voxel3Dx)));
 maxv = max(voxels_voted(:));
 fid = figure;
 for j=1:size(voxels_voted1,3)  
     figure(fid), imagesc((squeeze(voxels_voted1(:,:,j))), [0 maxv]), title([num2str(j), ' - press any key to continue']), axis equal, 
     pause,
 end

%% 6 apply marching cube algorithm and display the result
error_amount = 5;
maxv = max(voxels_voted(:,4));
iso_value = maxv-round(((maxv)/100)*error_amount)-0.5;
disp(['max number of votes:' num2str(maxv)])
disp(['threshold for marching cube:' num2str(iso_value)]);

[voxel3D] = ConvertVoxelList2Voxel3D(voxels_number, voxel_size, voxels_voted);

[fv]  = isosurface(voxel3Dx, voxel3Dy, voxel3Dz, voxel3D, iso_value, voxel3Dz);
[faces, verts, colors]  = isosurface(voxel3Dx, voxel3Dy, voxel3Dz, voxel3D, iso_value, voxel3Dz);

verts_min =  min(verts);
verts_max =  max(verts);
verts_diff = abs(verts_max-verts_min);

verts(:,1) = verts(:,1) - verts_min(1)-verts_diff(1)/2;
verts(:,2) = verts(:,2) - verts_min(2)-verts_diff(2)/2;

fv.vertices = verts;
verts = verts/max(verts_max);


fid = figure; 
p=patch('vertices', verts, 'faces', faces, ... 
    'facevertexcdata', colors, ... 
    'facecolor','flat', ... 
    'edgecolor', 'interp');

set(p,'FaceColor', [0.5 0.5 0.5], 'FaceLighting', 'flat',...
    'EdgeColor', 'none', 'SpecularStrength', 0, 'AmbientStrength', 0.4, 'DiffuseStrength', 0.6);

set(gca,'DataAspectRatio',[1 1 1], 'PlotBoxAspectRatio',[1 1 1],...
    'PlotBoxAspectRatioMode', 'manual');

axis vis3d;

light('Position',[1 1 0.5], 'Visible', 'on');
light('Position',[1 -1 0.5], 'Visible', 'on');
light('Position',[-1 1 0.5], 'Visible', 'on');
light('Position',[-1 -1 0.5], 'Visible', 'on'); 

ka = 0.1; kd = 0.4; ks = 0;
material([ka kd ks])

axis equal;
axis tight
axis off

%% 7 save VH to stl file
data_dir = '/Users/yuminggu/Desktop/vgl_project/lightstage-mingminghe/owen/';
file_base = 'newtest';
cdate = datestr(now, 'yyyy.mm.dd');
filename = [data_dir file_base '_VH_' cdate '.stl'];
patch2stl(filename, fv);