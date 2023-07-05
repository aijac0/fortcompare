module triangles
    implicit none

    ! Triangle with real side lengths
    logical :: calc_real_triangle
    real, dimension(3) :: t1
    real, dimension(3) :: t2
    real, dimension(3) :: t3
    real :: t1_area, t2_area, t3_area
    character(32) :: output_real_triangle

    ! Triangle with integer side lengths
    logical :: calc_int_triangle
    integer, dimension(3) :: int_t1
    integer, dimension(3) :: int_t2
    integer, dimension(3) :: int_t3
    real :: int_t1_area, int_t2_area, int_t3_area
    character(32) :: output_int_triangle

    ! Right triangles with real side lengths
    logical :: calc_real_right_triangle
    real, dimension(3) :: right_t1
    real, dimension(3) :: right_t2
    real, dimension(3) :: right_t3
    real :: right_t1_area, right_t2_area, right_t3_area
    character(32) :: output_real_right_triangle

    ! Right triangles with integer side lengths
    logical :: calc_int_right_triangle
    integer, dimension(3) :: int_right_t1
    integer, dimension(3) :: int_right_t2
    integer, dimension(3) :: int_right_t3
    real :: int_right_t1_area, int_right_t2_area, int_right_t3_area
    character(32) :: output_int_right_triangle

contains

    subroutine init_triangles
        implicit none
        
        ! Triangle with real side lengths
        calc_real_triangle = .true.
        t1 = (/13.4, 22.8, 28.6/)
        t2 = (/205.8, 131.9, 337.6/)
        t3 = (/1414.8, 780.4, 634.5/)
        t1_area = 0
        t2_area = 0
        t3_area = 0
        output_real_triangle = "Not computed"

        ! Triangle with integer side lengths
        calc_int_triangle = .true.
        int_t1 = (/14, 19, 20/)
        int_t2 = (/128, 146, 273/)
        int_t3 = (/986, 1008, 23/)
        int_t1_area = 0 
        int_t2_area = 0 
        int_t3_area = 0 
        output_int_triangle = "Not computed"

        ! Right triangles with real side lengths
        calc_real_right_triangle = .true.
        right_t1 = (/3.1, 4.6, 5.5/)
        right_t2 = (/8.6, 6.5, 10.8/)
        right_t3 = (/892.5, 328.8, 951.1/)
        right_t1_area = 0
        right_t2_area = 0
        right_t3_area = 0
        output_real_right_triangle = "Not computed"

        ! Right triangles with integer side lengths
        calc_int_right_triangle = .true.
        int_right_t1 = (/3, 4, 5/)
        int_right_t2 = (/351, 468, 585/)
        int_right_t3 = (/3255, 4340, 5425/)
        int_right_t1_area = 0
        int_right_t2_area = 0
        int_right_t3_area = 0
        output_int_right_triangle = "Not computed"
        

    end subroutine

end module
