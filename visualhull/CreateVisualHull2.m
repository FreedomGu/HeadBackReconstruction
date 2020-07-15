function [voxels] = CreateVisualHull2(silhouettes, voxels, params, display_projected_voxels,silhouettes2, params2)

if ~exist('display_projected_voxels', 'var')
    display_projected_voxels = 0;
end

if(display_projected_voxels == 1)
    fid = figure;
end

object_points3D = [voxels(:,1)'; voxels(:,2)'; voxels(:,3)'; ones(1, length(voxels))];
voxels(:, 4) = zeros(size(voxels(:, 4)));
disp(size(params));
fprintf('frames:');
for i = 1:size(params,3)
    fprintf(1, ' %i', i);    
    
    M = params(:,:,i);

    % projecting voxels centers to image    
    points2D = M*object_points3D;
    disp("points2d:"+size(points2D))
    object_points_cam = floor(points2D./[points2D(3,:); points2D(3,:); points2D(3,:)]);
    object_points_cam(object_points_cam <= 0) = 1;
    % insure that projected voxels are inside image
    img_size = size(silhouettes);
    ind1 = find(object_points_cam(2,:)>img_size(1));
    object_points_cam(:,ind1) = 1;
    ind1 = find(object_points_cam(1,:)>img_size(2));
    object_points_cam(:,ind1) = 1;
    disp("object_point:"+size(object_points_cam(2,:)'));
    % increase counter of each voxel for object pixel
    ind = int32(sub2ind(img_size(1:2), object_points_cam(2,:)',object_points_cam(1,:)'));    
    %disp("ind:"+ind);
    cur_silhouette = silhouettes(:,:,i);
    disp("ind:" + cur_silhouette(272161));
    img_val = cur_silhouette(uint32(ind));
    disp("img_val:"+ size(img_val));
    voxels([1:numel(img_val)], 4) = voxels([1:numel(img_val)], 4) + img_val(:);
    if(display_projected_voxels)
        img = figure(fid), imagesc(cur_silhouette);title(i);
        hold on
        plot(object_points_cam(1,:), object_points_cam(2,:), '.g')
        hold off
        filename ='/Users/yuminggu/Desktop/lightstage-mingminghe/visualize2/';
        disp(filename);
        saveas(img,[filename num2str(i) '.png']);
    end
end  
for j = 1:size(params2,3)
    fprintf(1, ' %i', j);
    M = params2(:,:,j);
    points2D = M*object_points3D;
    object_points_cam = floor(points2D./[points2D(3,:); points2D(3,:); points2D(3,:)]);
    object_points_cam(object_points_cam <= 0) = 1;
    img_size = size(silhouettes2);
    ind1 = find(object_points_cam(2,:)>img_size(1));
    object_points_cam(:,ind1) = 1;
    ind1 = find(object_points_cam(1,:)>img_size(2));
    object_points_cam(:,ind1) = 1;
    indx = int32(sub2ind(img_size(1:2), object_points_cam(2,:)',object_points_cam(1,:)'));
    cur_silhouette = silhouettes2(:,:,j);
    img_valx = cur_silhouette(uint32(indx));
    disp("img_val:" + size(img_valx));
    voxels([1:numel(img_valx)],4) = voxels([1:numel(img_valx)],4)+img_val(:);
    if(display_projected_voxels)
        figure(fid), imagesc(cur_silhouette);title(j);
        hold on
        plot(object_points_cam(1,:), object_points_cam(2,:), '.g')
        hold off
        saveas(img,[filename 'stage' num2str(j) '.png'])
        % pause;
    end
end
fprintf(1, '\n');